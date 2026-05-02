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

ASSISTANT_ID = "stock-assistant"
ASSISTANT_NAME = "Stock Assistant"

IDENTITY = AssistantIdentity(
    id=ASSISTANT_ID,
    name=ASSISTANT_NAME,
    metadata={},
)

SYSTEM_PROMPT = (
    "You are the Stock Assistant — a market-watching agent. "
    "You answer stock and trading questions concisely. "
    "When you proactively open a thread with a user (via the alert webhook), "
    "briefly explain why you're reaching out before waiting for a reply."
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

    @client.on_message()
    async def respond(ctx: HandlerContext, send: Send):
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

        async with send.message_stream() as stream:
            async for delta in provider.stream(system=SYSTEM_PROMPT, messages=messages, tools=[]):
                if delta.text:
                    await stream.write(delta.text)
