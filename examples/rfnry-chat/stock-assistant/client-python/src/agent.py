from __future__ import annotations

from rfnry_chat_client import ChatClient, HandlerContext, Send
from rfnry_chat_protocol import AssistantIdentity, TextPart

from src import provider

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


def register(client: ChatClient) -> None:
    anthropic = provider.build_anthropic()

    @client.on_message()
    async def respond(ctx: HandlerContext, send: Send):
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

        async with send.message_stream() as stream:
            async with anthropic.messages.stream(
                model=provider.ANTHROPIC_MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=messages,
            ) as model_stream:
                async for token in model_stream.text_stream:
                    await stream.write(token)
