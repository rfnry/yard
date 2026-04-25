from __future__ import annotations

from rfnry_chat_client import ChatClient, HandlerContext, HandlerSend
from rfnry_chat_protocol import AssistantIdentity, TextPart

from src import provider
from src.mentions import parse_member_mentions

ASSISTANT_ID = "agent-a"
ASSISTANT_NAME = "Agent A"

PERSONA_PROMPT = (
    "You are Agent A, an Engineering Manager AI on this team's chat. "
    "You're direct, terse, and code-aware. You write like an engineer who's "
    "busy but cares — short, no fluff, action-oriented. Avoid emojis. "
    "When you proactively reach out (via a webhook-triggered ping), briefly "
    "state what's on your mind and invite a reply."
    "\n\nWhen replying in a channel, you can address a specific teammate by "
    "prefixing your message with @<their-name> (e.g. '@Agent B can you take this?'). "
    "Only that teammate will receive your reply. Without an @-prefix, your reply goes "
    "to the entire channel."
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
        # Suppress agent-to-agent loops in shared channels. The library already
        # blocks self-triggering (author.id != self.id), but nothing stops
        # agent-b from responding to agent-a's messages — which would cascade
        # until MAX_HANDLER_CHAIN_DEPTH. Responding only to user-authored
        # messages keeps agents "human-facing" without losing any intended UX.
        # lazy_run=True: defer begin_run to first yield so sibling-agent messages
        # that hit this guard don't produce phantom run.started / run.completed.
        if ctx.event.author.role != "user":
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

        # Determine whether this is a channel thread so we can parse @-mentions.
        thread = await client.rest.get_thread(ctx.event.thread_id)
        kind = (thread.metadata or {}).get("kind") if thread else None
        is_channel = kind == "channel"

        members_page = await client.rest.list_members(ctx.event.thread_id) if is_channel else []
        members_list = [m.identity for m in members_page] if is_channel else []

        # Check for a leading @-mention in the model's first text block.
        # We need the full text upfront to extract recipients before publishing,
        # so the mention path uses a non-streaming call. The broadcast path
        # (channel without @-mention, or DM) streams token-by-token.
        response = await provider.call(
            anthropic,
            messages=messages,
            system_prompt=PERSONA_PROMPT,
        )
        first_text = next(
            (
                getattr(b, "text", "")
                for b in response.content
                if getattr(b, "type", None) == "text" and getattr(b, "text", "")
            ),
            "",
        )
        if is_channel and first_text:
            parsed = parse_member_mentions(first_text, members_list)
            if parsed.recipients:
                # Mention path: emit non-streamed blocks with recipients set.
                yield send.message(
                    content=[TextPart(text=parsed.text_without_leading_mentions)],
                    recipients=parsed.recipients,
                )
                for b in response.content[1:]:
                    extra = getattr(b, "text", "")
                    if getattr(b, "type", None) == "text" and extra:
                        yield send.message(
                            content=[TextPart(text=extra)],
                            recipients=parsed.recipients,
                        )
                return

        # Broadcast path: stream the response token-by-token.
        async with send.message_stream() as stream:
            async with anthropic.messages.stream(
                model=provider.ANTHROPIC_MODEL,
                max_tokens=provider.ANTHROPIC_MAX_TOKENS,
                system=PERSONA_PROMPT,
                messages=messages,
            ) as model_stream:
                async for token in model_stream.text_stream:
                    await stream.write(token)
