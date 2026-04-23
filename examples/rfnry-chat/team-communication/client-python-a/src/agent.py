from __future__ import annotations

from rfnry_chat_client import ChatClient, HandlerContext, HandlerSend
from rfnry_chat_protocol import AssistantIdentity, TextPart

from src import provider

ASSISTANT_ID = "agent-a"
ASSISTANT_NAME = "Agent A"

PERSONA_PROMPT = (
    "You are Agent A, an Engineering Manager AI on this team's chat. "
    "You're direct, terse, and code-aware. You write like an engineer who's "
    "busy but cares — short, no fluff, action-oriented. Avoid emojis. "
    "When you proactively reach out (via a webhook-triggered ping), briefly "
    "state what's on your mind and invite a reply."
)

SUBJECTS: list[str] = [
    "PR-1234 (refactor auth middleware) is ready for review",
    "main is red — flake on test_thread_invited",
    "design doc for the presence system landed in chat/docs",
    "p99 latency on /chat/threads doubled overnight — looking into it",
    "we should split the ChatServer god-class before it grows again",
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
        # Suppress agent-to-agent loops in shared channels. The library already
        # blocks self-triggering (author.id != self.id), but nothing stops
        # agent-b from responding to agent-a's messages — which would cascade
        # until MAX_HANDLER_CHAIN_DEPTH. Responding only to user-authored
        # messages keeps agents "human-facing" without losing any intended UX.
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
