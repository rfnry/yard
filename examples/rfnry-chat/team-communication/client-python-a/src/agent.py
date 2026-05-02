from __future__ import annotations

import os

from pydantic import SecretStr
from rfnry_chat_client import ChatClient, HandlerContext, Send
from rfnry_chat_client.providers import (
    AnthropicConfig,
    MockConfig,
    TextMessages,
    events_to_messages,
    last_user_text,
    resolve_text_messages,
)
from rfnry_chat_protocol import AssistantIdentity, TextPart

ASSISTANT_ID = "engineer"
ASSISTANT_NAME = "Engineer"

PERSONA_PROMPT = (
    "You are Engineer, an Engineering Manager AI on this team's chat. "
    "You're direct, terse, and code-aware. You write like an engineer who's "
    "busy but cares — short, no fluff, action-oriented. Avoid emojis. "
    "When you proactively reach out (via a webhook-triggered ping), briefly "
    "state what's on your mind and invite a reply."
    "\n\n"
    "When you want to address a teammate directly in a channel, write "
    "@<their handle> somewhere in your message. The system reads the @<handle> "
    "tokens and routes the message to those teammates.\n"
    "\n"
    "Available teammates and their handles:\n"
    "  - @engineer (you)\n"
    "  - @coordinator (Release Coordinator)\n"
    "  - @liaison (Support Liaison)\n"
    "  - User handles look like u_<id> — match the @<handle> the user used "
    "when pinging you, or omit and the system will route to whoever pinged.\n"
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


def build_provider() -> TextMessages:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("ANTHROPIC_API_KEY unset — provider stubbed via MockConfig")
        return resolve_text_messages(MockConfig(model="mock-claude"))
    return resolve_text_messages(
        AnthropicConfig(api_key=SecretStr(api_key), model="claude-sonnet-4-5-20250929")
    )


def register(client: ChatClient) -> None:
    provider = build_provider()

    @client.on_message(lazy_run=True)
    async def respond(ctx: HandlerContext, send: Send):
        if ctx.event.author.role != "user":
            return

        thread = await client.rest.get_thread(ctx.event.thread_id)
        is_channel = (thread.metadata or {}).get("kind") == "channel"
        if is_channel and IDENTITY.id not in (ctx.event.recipients or []):
            return

        history_page = await client.rest.list_events(ctx.event.thread_id, limit=200)
        history = history_page["items"]
        messages = events_to_messages(history, self_id=IDENTITY.id)
        if not messages:
            return

        if provider.kind == "mock":
            yield send.message(
                content=[
                    TextPart(
                        text=(
                            f"[stub reply from {IDENTITY.name} — set ANTHROPIC_API_KEY "
                            f"to wire the real model] you said: "
                            f"{last_user_text(history, self_id=IDENTITY.id)}"
                        )
                    )
                ]
            )
            return

        recipients = [ctx.event.author.id] if is_channel else None

        async with send.message_stream(recipients=recipients) as stream:
            async for delta in provider.stream(system=PERSONA_PROMPT, messages=messages, tools=[]):
                if delta.text:
                    await stream.write(delta.text)
