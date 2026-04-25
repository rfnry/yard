from __future__ import annotations

from rfnry_chat_client import ChatClient, HandlerContext, HandlerSend
from rfnry_chat_protocol import AssistantIdentity, TextPart

from src import provider
from src.mentions import parse_member_mentions

ASSISTANT_ID = "agent-b"
ASSISTANT_NAME = "Agent B"

PERSONA_PROMPT = (
    "You are Agent B, the Release Coordinator. You're calm, process-y, and "
    "calendar-aware. You speak in dates and gates. You write like someone "
    "keeping the trains running. Avoid emojis. When you proactively reach "
    "out (via a webhook-triggered ping), briefly state what's on your mind "
    "and invite a reply."
    "\n\nWhen replying in a channel, you can address a specific teammate by "
    "prefixing your message with @<their-name> (e.g. '@Agent B can you take this?'). "
    "Only that teammate will receive your reply. Without an @-prefix, your reply goes "
    "to the entire channel."
)

SUBJECTS: list[str] = [
    "release cut for v0.42 moves to Friday — engineering needs to land 3 PRs by EOD Thu",
    "merge freeze starts tomorrow at 17:00 UTC for the mobile branch",
    "pre-prod canary is at 5% and clean for 2h — ready to ramp to 25%",
    "the rollback runbook is stale — last update was 6 months ago",
    "all green on the release dashboard, we're ship-ready",
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

        # Check for a leading @-mention in the model's first text block.
        # We need the full text upfront to extract recipients before publishing,
        # so the mention path uses a non-streaming call. The broadcast path
        # (channel without @-mention, or DM) streams token-by-token.
        response = await provider.call(
            anthropic,
            messages=messages,
            system_prompt=PERSONA_PROMPT,
        )
        first_text = next(
            (
                getattr(b, "text", "")
                for b in response.content
                if getattr(b, "type", None) == "text" and getattr(b, "text", "")
            ),
            "",
        )
        if is_channel and first_text:
            parsed = parse_member_mentions(first_text, members_list)
            if parsed.recipients:
                # Mention path: emit non-streamed blocks with recipients set.
                yield send.message(
                    content=[TextPart(text=parsed.text_without_leading_mentions)],
                    recipients=parsed.recipients,
                )
                for b in response.content[1:]:
                    extra = getattr(b, "text", "")
                    if getattr(b, "type", None) == "text" and extra:
                        yield send.message(
                            content=[TextPart(text=extra)],
                            recipients=parsed.recipients,
                        )
                return

        # Broadcast path: stream the response token-by-token.
        async with send.message_stream() as stream:
            async with anthropic.messages.stream(
                model=provider.ANTHROPIC_MODEL,
                max_tokens=provider.ANTHROPIC_MAX_TOKENS,
                system=PERSONA_PROMPT,
                messages=messages,
            ) as model_stream:
                async for token in model_stream.text_stream:
                    await stream.write(token)
