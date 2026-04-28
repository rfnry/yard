from __future__ import annotations

from rfnry_chat_client import ChatClient

from src.agent import IDENTITY


async def join_all_channels(client: ChatClient) -> None:
    page = await client.rest.list_threads()
    for thread in page["items"]:
        kind = (thread.metadata or {}).get("kind")
        if kind != "channel":
            continue
        await client.join_thread(thread.id)
        print(f"{IDENTITY.name} joined channel thread={thread.id}")


def register(client: ChatClient) -> None:
    @client.on_invited()
    async def _on_invited(frame) -> None:  # type: ignore[no-untyped-def]
        kind = (frame.thread.metadata or {}).get("kind")
        print(f"{IDENTITY.name} invited to thread={frame.thread.id} kind={kind}")
