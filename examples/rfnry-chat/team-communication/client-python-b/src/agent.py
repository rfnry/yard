from __future__ import annotations

from rfnry_chat_client import ChatClient, HandlerContext, HandlerSend
from rfnry_chat_protocol import AssistantIdentity, TextPart

from src import provider

ASSISTANT_ID = "agent-b"
ASSISTANT_NAME = "Agent B"

PERSONA_PROMPT = (
    "You are Agent B, the Release Coordinator. You're calm, process-y, and "
    "calendar-aware. You speak in dates and gates. You write like someone "
    "keeping the trains running. Avoid emojis. When you proactively reach "
    "out (via a webhook-triggered ping), briefly state what's on your mind "
    "and invite a reply."
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

    @client.on_message()
    async def respond(ctx: HandlerContext, send: HandlerSend):
        # Suppress agent-to-agent loops in shared channels (see client-python-a).
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

        response = await provider.call(
            anthropic,
            messages=messages,
            system_prompt=PERSONA_PROMPT,
        )
        for block in response.content:
            text = getattr(block, "text", "")
            if getattr(block, "type", None) == "text" and text:
                yield send.message(content=[TextPart(text=text)])
