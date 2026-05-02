from __future__ import annotations

import random

from rfnry_chat_client import Send
from rfnry_chat_client.providers import Message
from rfnry_chat_protocol import TextPart

from src.agent import IDENTITY, PERSONA_PROMPT, SUBJECTS, build_provider


async def stream_proactive_message(
    send: Send,
    *,
    audience: str,
    addressee_name: str,
    mention_inline: bool,
    addressee_id: str | None = None,
) -> str:
    subject = random.choice(SUBJECTS)
    provider = build_provider()

    if provider.kind == "mock":
        await send.emit(
            send.message([TextPart(text=f"[stub {IDENTITY.name}] subject: {subject}")]),
        )
        return subject

    if mention_inline and addressee_id:
        addressing = f"Mention them inline as @{addressee_id}."
    else:
        addressing = f"Address them once as {addressee_name}."
    user_prompt = (
        f"You are reaching out proactively to {addressee_name} via a {audience}. "
        f"The topic on your mind: {subject}\n\n"
        f"Write a single short chat message (1-3 sentences) opening the conversation. "
        f"Stay in character. Don't double-greet. {addressing}"
    )

    recipients = [addressee_id] if audience == "channel" and addressee_id else None

    async with send.message_stream(recipients=recipients) as stream:
        async for delta in provider.stream(
            system=PERSONA_PROMPT,
            messages=[Message(role="user", content=user_prompt)],
            tools=[],
        ):
            if delta.text:
                await stream.write(delta.text)

    return subject
