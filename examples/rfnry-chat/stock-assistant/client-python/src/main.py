from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rfnry_chat_client import ChatClient

from src import webhooks
from src.agent import IDENTITY, register

CHAT_SERVER_URL = os.environ.get("CHAT_SERVER_URL", "http://127.0.0.1:8000")
PORT = int(os.environ.get("PORT", "9100"))

client = ChatClient(base_url=CHAT_SERVER_URL, identity=IDENTITY, data_root=Path("./var"))
register(client)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    async with client.running():
        yield


app = FastAPI(title="stock-assistant-agent", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
webhooks.register(app, client)

if __name__ == "__main__":
    import uvicorn

    print(f"stock-assistant agent connecting to {CHAT_SERVER_URL} as {IDENTITY.id}")
    try:
        uvicorn.run(app, host="0.0.0.0", port=PORT)
    except asyncio.CancelledError:
        pass
