from __future__ import annotations

from datetime import UTC, datetime

from rfnry_chat_protocol import Identity, Thread
from rfnry_chat_server import (
    ChatServer,
    ChatStore,
    HandlerContext,
    HandlerSend,
    MessageEvent,
)

# Pre-created channel threads. The tuple is (thread_id, channel_slug, label).
CHANNELS: list[tuple[str, str, str]] = [
    ("ch_general", "general", "General team chat"),
    ("ch_engineering", "engineering", "Engineering"),
]


async def _authorize(
    identity: Identity,
    thread_id: str,
    action: str,
    *,
    store: ChatStore,
    target_id: str | None = None,
) -> bool:
    """Hybrid policy:
    - Channel threads (metadata.kind == "channel"): public. Anyone whose
      tenant matches the thread's tenant via `matches()` (already checked
      by the core before authorize fires) can read/write.
    - DM threads (metadata.kind == "dm"): membership-based. Only members
      can read/write.
    """
    del action, target_id
    thread = await store.get_thread(thread_id)
    if thread is None:
        return False
    kind = (thread.metadata or {}).get("kind")
    if kind == "channel":
        return True
    return await store.is_member(thread_id, identity.id)


async def bootstrap_channels(store: ChatStore) -> None:
    """Idempotently create the configured channel threads."""
    now = datetime.now(UTC)
    for thread_id, slug, label in CHANNELS:
        existing = await store.get_thread(thread_id)
        if existing is not None:
            continue
        await store.create_thread(
            Thread(
                id=thread_id,
                tenant={"channel": slug},
                metadata={"kind": "channel", "label": label},
                created_at=now,
                updated_at=now,
            )
        )
        print(f"bootstrap: created channel thread={thread_id} slug={slug}")


def create_chat_server(store: ChatStore) -> ChatServer:
    # Close the store into _authorize so the callback has access to it.
    async def _authorize_with_store(
        identity: Identity,
        thread_id: str,
        action: str,
        *,
        target_id: str | None = None,
    ) -> bool:
        return await _authorize(identity, thread_id, action, store=store, target_id=target_id)

    chat_server = ChatServer(store=store, authorize=_authorize_with_store)

    @chat_server.on_message()
    async def log_message(ctx: HandlerContext, _send: HandlerSend) -> None:
        assert isinstance(ctx.event, MessageEvent)
        preview = next(
            (getattr(p, "text", "") for p in ctx.event.content if getattr(p, "type", None) == "text"),
            "",
        )
        kind = (ctx.thread.metadata or {}).get("kind", "?")
        print(
            f"msg kind={kind} thread={ctx.thread.id} "
            f"author={ctx.event.author.id} preview={preview[:60]!r}"
        )

    return chat_server
