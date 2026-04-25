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
    """Post a proactively-composed message into ``thread_id``.

    On success, streams the reply token-by-token via ``stream:start`` /
    ``:delta`` / ``:end`` frames. On the stub path (``ANTHROPIC_API_KEY``
    unset) sends a one-shot fallback message so routing still demos without
    an API key.

    Parameters
    ----------
    client:
        Connected ``ChatClient`` used to open the run and emit frames.
    thread_id:
        Target thread.
    audience:
        ``"channel"`` or ``"direct DM"`` — shaped into the user prompt so
        the model picks an appropriate tone.
    addressee_name:
        Display name of the person/agent being addressed.
    mention_inline:
        ``True`` for channel pings (``@name`` mention), ``False`` for DMs
        (address once by name, no mention).
    addressee_id:
        Identity id of the addressee. When ``audience == "channel"``, sets
        ``recipients=[addressee_id]`` on the stream so other agents stay
        silent while the pinged user can still see the deltas.

    Returns
    -------
    str
        The subject that was picked (useful for logging/response bodies).
    """
    subject = random.choice(SUBJECTS)
    anthropic = provider.build_anthropic()

    if anthropic is None:
        # Stub: skip streaming, post a single placeholder.
        await client.send_message(
            thread_id,
            content=[TextPart(text=f"[stub {IDENTITY.name}] subject: {subject}")],
        )
        return subject

    addressing = (
        f"Mention them inline as @{addressee_name}." if mention_inline else f"Address them once as {addressee_name}."
    )
    user_prompt = (
        f"You are reaching out proactively to {addressee_name} via a {audience}. "
        f"The topic on your mind: {subject}\n\n"
        f"Write a single short chat message (1-3 sentences) opening the conversation. "
        f"Stay in character. Don't double-greet. {addressing}"
    )

    # Channel pings route the final event to the specific addressee so other
    # agents don't react. Deltas remain visible to all room members.
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
