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

SYSTEM_PROMPT = "You are a customer support assistant. Answer user questions concisely and politely."


def build_provider() -> TextMessages:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("ANTHROPIC_API_KEY unset — provider stubbed via MockConfig")
        return resolve_text_messages(MockConfig(model="mock-claude"))
    return resolve_text_messages(
        AnthropicConfig(api_key=SecretStr(api_key), model="claude-sonnet-4-5-20250929")
    )


def register(chat_client: ChatClient, identity: AssistantIdentity) -> None:
    provider = build_provider()

    @chat_client.on_message()
    async def handle_message(ctx: HandlerContext, send: Send):
        history_page = await chat_client.rest.list_events(ctx.event.thread_id, limit=200)
        history = history_page["items"]
        messages = events_to_messages(history, self_id=identity.id)
        if not messages:
            return

        if provider.kind == "mock":
            yield send.message(
                content=[
                    TextPart(
                        text=(
                            f"[stub reply from {identity.name} — set ANTHROPIC_API_KEY "
                            f"to wire the real model] you said: "
                            f"{last_user_text(history, self_id=identity.id)}"
                        )
                    )
                ]
            )
            return

        reply = await provider.generate(system=SYSTEM_PROMPT, messages=messages, tools=[])
        if reply.text:
            yield send.message(content=[TextPart(text=reply.text)])
