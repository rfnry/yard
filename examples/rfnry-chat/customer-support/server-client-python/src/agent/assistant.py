from __future__ import annotations

from rfnry_chat_client import ChatClient, HandlerContext, HandlerSend
from rfnry_chat_protocol import AssistantIdentity, TextPart

from src.agent import provider

SYSTEM_PROMPT = "You are a customer support assistant. Answer user questions concisely and politely."


def register(chat_client: ChatClient, identity: AssistantIdentity) -> None:
    anthropic = provider.build_anthropic()

    @chat_client.on_message()
    async def handle_message(ctx: HandlerContext, send: HandlerSend):
        history_page = await chat_client.rest.list_events(ctx.event.thread_id, limit=200)
        history = history_page["items"]
        messages = provider.to_anthropic_messages(history, identity.id)
        if not messages:
            return

        if anthropic is None:
            yield send.message(
                content=[
                    TextPart(
                        text=(
                            f"[stub reply from {identity.name} — set ANTHROPIC_API_KEY "
                            f"to wire the real model] you said: "
                            f"{provider.last_user_text(history, identity.id)}"
                        )
                    )
                ]
            )
            return

        response = await provider.call(
            anthropic,
            messages=messages,
            system_prompt=SYSTEM_PROMPT,
        )
        for block in response.content:
            text = getattr(block, "text", "")
            if getattr(block, "type", None) == "text" and text:
                yield send.message(content=[TextPart(text=text)])
