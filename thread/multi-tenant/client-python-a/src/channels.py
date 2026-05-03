from __future__ import annotations

from rfnry_chat_client import ChatClient

_LABEL = "agent-a"
_joined_threads: set[str] = set()


async def join_all_threads(client: ChatClient) -> None:
    page = await client.rest.list_threads()
    for thread in page["items"]:
        if thread.id in _joined_threads:
            continue
        await client.join_thread(thread.id)
        _joined_threads.add(thread.id)
        print(f"{_LABEL} joined thread={thread.id} tenant={thread.tenant}")


def register(client: ChatClient) -> None:
    @client.on_invited()
    async def _on_invited(frame) -> None:  # type: ignore[no-untyped-def]
        _joined_threads.add(frame.thread.id)
        print(f"{_LABEL} invited to thread={frame.thread.id} tenant={frame.thread.tenant}")
