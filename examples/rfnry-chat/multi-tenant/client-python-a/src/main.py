from __future__ import annotations

import asyncio
import os

from rfnry_chat_client import ChatClient

from src.agent import IDENTITY, register

DEFAULT_BASE_URL = "http://127.0.0.1:8000"


async def _discover_and_join(client: ChatClient, joined: set[str]) -> None:
    """One-shot scan of tenant-visible threads at connect time.

    The sidebar's new-thread flow calls addMember(agent) which fires
    thread:invited to this agent's inbox; auto_join_on_invite handles the
    rest live. This one-time list_threads is here purely for recovery —
    e.g., an agent coming back up after a restart re-joining threads that
    already existed in the store.
    """
    page = await client.rest.list_threads()
    for thread in page["items"]:
        if thread.id in joined:
            continue
        await client.join_thread(thread.id)
        joined.add(thread.id)
        print(f"agent-a joined thread={thread.id} tenant={thread.tenant}")


async def main() -> None:
    base_url = os.environ.get("CHAT_SERVER_URL", DEFAULT_BASE_URL)
    client = ChatClient(base_url=base_url, identity=IDENTITY)
    register(client)
    joined: set[str] = set()

    async def on_connect() -> None:
        await _discover_and_join(client, joined)

    @client.on_invited()
    async def on_invited(frame):  # type: ignore[no-untyped-def]
        joined.add(frame.thread.id)
        print(f"agent-a invited to thread={frame.thread.id} tenant={frame.thread.tenant}")

    print(f"agent-a connecting to {base_url} as {IDENTITY.id} (tenant={IDENTITY.metadata['tenant']})")
    await client.run(on_connect=on_connect)


if __name__ == "__main__":
    asyncio.run(main())
