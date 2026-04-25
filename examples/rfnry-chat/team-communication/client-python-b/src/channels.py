from __future__ import annotations

from rfnry_chat_client import ChatClient

from src.agent import IDENTITY

_joined_threads: set[str] = set()


async def join_all_channels(client: ChatClient) -> None:
    """One-shot scan of tenant-visible threads at connect time.

    Filters to `metadata.kind == "channel"` — DMs are joined reactively via
    the on_invited handler when a user starts a DM with this agent. See
    ../../multi-tenant/client-python-a/src/main.py for the reconnect-recovery
    rationale.
    """
    page = await client.rest.list_threads()
    for thread in page["items"]:
        kind = (thread.metadata or {}).get("kind")
        if kind != "channel":
            continue
        if thread.id in _joined_threads:
            continue
        await client.join_thread(thread.id)
        _joined_threads.add(thread.id)
        print(f"{IDENTITY.name} joined channel thread={thread.id}")


def register(client: ChatClient) -> None:
    @client.on_invited()
    async def _on_invited(frame) -> None:  # type: ignore[no-untyped-def]
        _joined_threads.add(frame.thread.id)
        kind = (frame.thread.metadata or {}).get("kind")
        print(f"{IDENTITY.name} invited to thread={frame.thread.id} kind={kind}")


def joined_threads() -> set[str]:
    """Live mutable reference to the joined-thread set, for webhook handlers
    that need to track state."""
    return _joined_threads
