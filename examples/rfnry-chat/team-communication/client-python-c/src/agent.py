from __future__ import annotations

from rfnry_chat_client import ChatClient, HandlerContext, HandlerSend
from rfnry_chat_protocol import AssistantIdentity, TextPart

from src import provider
from src.mentions import parse_member_mentions

ASSISTANT_ID = "agent-c"
ASSISTANT_NAME = "Agent C"

PERSONA_PROMPT = (
    "You are Agent C, the Support Liaison. You're empathetic and "
    "customer-voiced. You translate user pain into engineering-actionable "
    "summaries without losing the human signal. Avoid emojis. When you "
    "proactively reach out (via a webhook-triggered ping), briefly state "
    "what's on your mind and invite a reply."
    "\n\nWhen replying in a channel, you can address a specific teammate by "
    "prefixing your message with @<their-name> (e.g. '@Agent B can you take this?'). "
    "Only that teammate will receive your reply. Without an @-prefix, your reply goes "
    "to the entire channel."
)

SUBJECTS: list[str] = [
    "customer (Acme Co) reports threads disappearing on refresh — 3 tickets in the last hour",
    "T1 SLA is at 4h response for the new tier — we need an on-call rotation update",
    "user feedback this week: overwhelming positive on the streaming UX, ask for read receipts",
    "escalation: enterprise customer can't add members to threads — blocking their pilot",
    "reminder: support holiday coverage starts next Monday, who's available?",
]

IDENTITY = AssistantIdentity(
    id=ASSISTANT_ID,
    name=ASSISTANT_NAME,
    metadata={"tenant": {"channel": "*"}},
)


def register(client: ChatClient) -> None:
    anthropic = provider.build_anthropic()

    @client.on_message(lazy_run=True)
    async def respond(ctx: HandlerContext, send: HandlerSend):
        # Suppress agent-to-agent loops in shared channels (see client-python-a).
        # lazy_run=True: defer begin_run to first yield so sibling-agent messages
        # that hit this guard don't produce phantom run.started / run.completed.
        if ctx.event.author.role != "user":
            return
        history_page = await client.rest.list_events(ctx.event.thread_id, limit=200)
        history = history_page["items"]
        messages = provider.to_anthropic_messages(history, IDENTITY.id)
        if not messages:
            return

        if anthropic is None:
            yield send.message(
                content=[
                    TextPart(
                        text=(
                            f"[stub reply from {IDENTITY.name} — set ANTHROPIC_API_KEY "
                            f"to wire the real model] you said: "
                            f"{provider.last_user_text(history, IDENTITY.id)}"
                        )
                    )
                ]
            )
            return

        # Determine whether this is a channel thread so we can parse @-mentions.
        thread = await client.rest.get_thread(ctx.event.thread_id)
        kind = (thread.metadata or {}).get("kind") if thread else None
        is_channel = kind == "channel"

        members_page = await client.rest.list_members(ctx.event.thread_id) if is_channel else []
        members_list = [m.identity for m in members_page] if is_channel else []

        response = await provider.call(
            anthropic,
            messages=messages,
            system_prompt=PERSONA_PROMPT,
        )
        for block in response.content:
            text = getattr(block, "text", "")
            if getattr(block, "type", None) != "text" or not text:
                continue
            if is_channel:
                parsed = parse_member_mentions(text, members_list)
                yield send.message(
                    content=[TextPart(text=parsed.text_without_leading_mentions)],
                    recipients=parsed.recipients or None,
                )
            else:
                yield send.message(content=[TextPart(text=text)])
