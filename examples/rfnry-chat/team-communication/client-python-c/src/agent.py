from __future__ import annotations

from rfnry_chat_client import ChatClient, HandlerContext, HandlerSend
from rfnry_chat_protocol import AssistantIdentity, TextPart

from src import provider

ASSISTANT_ID = "agent-c"
ASSISTANT_NAME = "Agent C"

PERSONA_PROMPT = (
    "You are Agent C, the Support Liaison. You're empathetic and "
    "customer-voiced. You translate user pain into engineering-actionable "
    "summaries without losing the human signal. Avoid emojis. When you "
    "proactively reach out (via a webhook-triggered ping), briefly state "
    "what's on your mind and invite a reply."
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

    @client.on_message()
    async def respond(ctx: HandlerContext, send: HandlerSend):
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

        response = await provider.call(
            anthropic,
            messages=messages,
            system_prompt=PERSONA_PROMPT,
        )
        for block in response.content:
            text = getattr(block, "text", "")
            if getattr(block, "type", None) == "text" and text:
                yield send.message(content=[TextPart(text=text)])
