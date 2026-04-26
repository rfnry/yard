from __future__ import annotations

import random
from typing import TYPE_CHECKING

from rfnry_chat_client.handler.send import HandlerSend
from rfnry_chat_protocol import RunError, TextPart

from src import provider
from src.agent import IDENTITY, PERSONA_PROMPT, SUBJECTS

if TYPE_CHECKING:
    from rfnry_chat_client import ChatClient


async def stream_proactive_message(
    client: ChatClient,
    *,
    thread_id: str,
    audience: str,
    addressee_name: str,
    mention_inline: bool,
    addressee_id: str | None = None,
) -> str:

    subject = random.choice(SUBJECTS)
    anthropic = provider.build_anthropic()

    if anthropic is None:
        await client.send_message(
            thread_id,
            content=[TextPart(text=f"[stub {IDENTITY.name}] subject: {subject}")],
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

    run_id = await client.begin_run(thread_id)
    try:
        send = HandlerSend(
            thread_id=thread_id,
            author=IDENTITY,
            client=client,
            run_id=run_id,
        )
        stream = send.message_stream(recipients=recipients)
        async with stream as s:
            async with anthropic.messages.stream(
                model=provider.ANTHROPIC_MODEL,
                max_tokens=512,
                system=PERSONA_PROMPT,
                messages=[{"role": "user", "content": user_prompt}],
            ) as model_stream:
                async for token in model_stream.text_stream:
                    await s.write(token)
        await client.end_run(run_id)
    except Exception as exc:
        await client.end_run(
            run_id,
            error=RunError(code="ping_failed", message=str(exc)),
        )
        raise

    return subject
