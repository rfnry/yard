from __future__ import annotations

import asyncio
import os
from pathlib import Path

from rfnry_chat_client import ChatClient

from src import channels
from src.agent import IDENTITY, register

DEFAULT_BASE_URL = "http://127.0.0.1:8000"


async def main() -> None:
    base_url = os.environ.get("CHAT_SERVER_URL", DEFAULT_BASE_URL)
    client = ChatClient(base_url=base_url, identity=IDENTITY, data_root=Path("./var/agent-a"))
    register(client)
    channels.register(client)

    print(f"agent-a connecting to {base_url} as {IDENTITY.id} (tenant={IDENTITY.metadata['tenant']})")
    await client.run(on_connect=lambda: channels.join_all_threads(client))


if __name__ == "__main__":
    asyncio.run(main())
