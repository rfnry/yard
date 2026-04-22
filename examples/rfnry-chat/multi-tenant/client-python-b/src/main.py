from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

import asyncio  # noqa: E402
import os  # noqa: E402

from rfnry_chat_client import ChatClient  # noqa: E402

from src.agent import IDENTITY, register  # noqa: E402

DEFAULT_BASE_URL = "http://127.0.0.1:8000"


async def _discover_and_join(client: ChatClient, joined: set[str]) -> None:
    page = await client.rest.list_threads()
    for thread in page["items"]:
        if thread.id in joined:
            continue
        await client.join_thread(thread.id)
        joined.add(thread.id)
        print(f"agent-b joined thread={thread.id} tenant={thread.tenant}")


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
        print(f"agent-b invited to thread={frame.thread.id} tenant={frame.thread.tenant}")

    print(f"agent-b connecting to {base_url} as {IDENTITY.id} (tenant={IDENTITY.metadata['tenant']})")
    await client.run(on_connect=on_connect)


if __name__ == "__main__":
    asyncio.run(main())
