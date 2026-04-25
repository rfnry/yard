from __future__ import annotations

import sys

from rfnry_chat_client import ChatClient, HandlerContext, HandlerSend, parse_member_mentions
from rfnry_chat_protocol import AssistantIdentity, TextPart

from src import provider

ASSISTANT_ID = "engineer"
ASSISTANT_NAME = "Engineer"

PERSONA_PROMPT = (
    "You are Engineer, an Engineering Manager AI on this team's chat. "
    "You're direct, terse, and code-aware. You write like an engineer who's "
    "busy but cares — short, no fluff, action-oriented. Avoid emojis. "
    "When you proactively reach out (via a webhook-triggered ping), briefly "
    "state what's on your mind and invite a reply."
    "\n\nWhen replying in a channel, ALWAYS begin your message with @<name> "
    "to address the right teammate (the user who pinged you, or another "
    "agent if you're handing off the conversation). The system uses this "
    "prefix to route the message — without it, the reply has no recipient "
    "and the system will fall back to replying to whoever pinged you."
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

    @client.on_message(lazy_run=True)
    async def respond(ctx: HandlerContext, send: HandlerSend):

        if ctx.event.author.role != "user":
            return

        thread = await client.rest.get_thread(ctx.event.thread_id)
        is_channel = (thread.metadata or {}).get("kind") == "channel"
        if is_channel and IDENTITY.id not in (ctx.event.recipients or []):
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

        members_page = await client.rest.list_members(ctx.event.thread_id) if is_channel else []
        members = [m.identity for m in members_page] if is_channel else []
        fallback_recipients = [ctx.event.author.id] if is_channel else None

        async with anthropic.messages.stream(
            model=provider.ANTHROPIC_MODEL,
            max_tokens=provider.ANTHROPIC_MAX_TOKENS,
            system=PERSONA_PROMPT,
            messages=messages,
        ) as model_stream:
            head_buffer = ""
            decided = False
            recipients: list[str] | None = None
            visible_head = ""
            BUFFER_LIMIT = 64

            stream_cm = None
            stream = None
            try:
                async for token in model_stream.text_stream:
                    if not decided:
                        head_buffer += token
                        stripped = head_buffer.lstrip()

                        if is_channel:
                            parsed = parse_member_mentions(stripped, members)
                            if parsed.recipients:
                                recipients = parsed.recipients
                                visible_head = parsed.body
                                decided = True
                            elif len(stripped) >= BUFFER_LIMIT or (stripped and not stripped.startswith("@")):
                                recipients = fallback_recipients
                                visible_head = head_buffer
                                decided = True
                        else:
                            recipients = None
                            visible_head = head_buffer
                            decided = True

                        if decided:
                            stream_cm = send.message_stream(recipients=recipients)
                            stream = await stream_cm.__aenter__()
                            if visible_head:
                                await stream.write(visible_head)

                        continue

                    await stream.write(token)

                if not decided:
                    return
            finally:
                if stream_cm is not None:
                    exc_info = sys.exc_info()
                    await stream_cm.__aexit__(*exc_info)
