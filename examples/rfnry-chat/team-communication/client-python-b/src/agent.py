from __future__ import annotations

import re
import sys

from rfnry_chat_client import ChatClient, HandlerContext, HandlerSend
from rfnry_chat_protocol import AssistantIdentity, TextPart

from src import provider

ASSISTANT_ID = "agent-b"
ASSISTANT_NAME = "Agent B"

PERSONA_PROMPT = (
    "You are Agent B, the Release Coordinator. You're calm, process-y, and "
    "calendar-aware. You speak in dates and gates. You write like someone "
    "keeping the trains running. Avoid emojis. When you proactively reach "
    "out (via a webhook-triggered ping), briefly state what's on your mind "
    "and invite a reply."
    "\n\nWhen replying in a channel, ALWAYS begin your message with @<name> "
    "to address the right teammate (the user who pinged you, or another "
    "agent if you're handing off the conversation). The system uses this "
    "prefix to route the message — without it, the reply has no recipient "
    "and the system will fall back to replying to whoever pinged you."
)

SUBJECTS: list[str] = [
    "release cut for v0.42 moves to Friday — engineering needs to land 3 PRs by EOD Thu",
    "merge freeze starts tomorrow at 17:00 UTC for the mobile branch",
    "pre-prod canary is at 5% and clean for 2h — ready to ramp to 25%",
    "the rollback runbook is stale — last update was 6 months ago",
    "all green on the release dashboard, we're ship-ready",
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
        # Suppress agent-to-agent loops in shared channels (see client-python-a).
        # lazy_run=True: defer begin_run to first yield so sibling-agent messages
        # that hit this guard don't produce phantom run.started / run.completed.
        if ctx.event.author.role != "user":
            return

        # Channels: respond ONLY when explicitly mentioned. Without a mention,
        # the agent stays silent — channels are watch-only until pinged.
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

        # Decide recipients up front by reading the model's leading text. We
        # buffer until we either find @<name> + whitespace, or commit to the
        # fallback (reply to whoever pinged us). Once decided, open the
        # message_stream and replay the buffered head + stream the rest live.
        members_page = await client.rest.list_members(ctx.event.thread_id) if is_channel else []
        members = [m.identity for m in members_page] if is_channel else []
        members_by_name = {m.name.lower(): m for m in members}
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
            BUFFER_LIMIT = 64  # commit to fallback after this many chars

            stream_cm = None
            stream = None
            try:
                async for token in model_stream.text_stream:
                    if not decided:
                        head_buffer += token
                        stripped = head_buffer.lstrip()
                        # Try mention extraction (only meaningful in channels).
                        if is_channel:
                            m = re.match(r"@([\w-]+)(\s+|$)", stripped)
                            if m and m.group(1).lower() in members_by_name:
                                target_id = members_by_name[m.group(1).lower()].id
                                recipients = [target_id]
                                # Strip the matched prefix from visible content.
                                visible_head = stripped[m.end():]
                                decided = True
                            elif len(stripped) >= BUFFER_LIMIT or (
                                stripped and not stripped.startswith("@")
                            ):
                                # No mention — fall back to original sender.
                                recipients = fallback_recipients
                                visible_head = head_buffer
                                decided = True
                        else:
                            # DM: no mention routing, single recipient implicit.
                            recipients = None
                            visible_head = head_buffer
                            decided = True

                        if decided:
                            stream_cm = send.message_stream(recipients=recipients)
                            stream = await stream_cm.__aenter__()
                            if visible_head:
                                await stream.write(visible_head)
                        # Otherwise keep buffering.
                        continue

                    # Stream is open; just forward.
                    await stream.write(token)

                # End-of-model-output: if we never decided (model produced no text),
                # close cleanly without emitting.
                if not decided:
                    return
            finally:
                if stream_cm is not None:
                    exc_info = sys.exc_info()
                    await stream_cm.__aexit__(*exc_info)
