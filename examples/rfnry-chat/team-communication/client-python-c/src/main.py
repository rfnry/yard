from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rfnry_chat_client import ChatClient

from src import agent, channels, webhooks
from src.agent import IDENTITY

CHAT_SERVER_URL = os.environ.get("CHAT_SERVER_URL", "http://127.0.0.1:8000")
PORT = int(os.environ.get("PORT", "9102"))


client = ChatClient(base_url=CHAT_SERVER_URL, identity=IDENTITY)
agent.register(client)
channels.register(client)


async def on_connect() -> None:
    await channels.join_all_channels(client)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    async with client.running(on_connect=on_connect):
        yield


app = FastAPI(title="team-communication-agent-c", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


webhooks.register(app, client)


if __name__ == "__main__":
    import uvicorn

    print(f"{IDENTITY.name} connecting to {CHAT_SERVER_URL} as {IDENTITY.id}")
    try:
        uvicorn.run(app, host="0.0.0.0", port=PORT)
    except asyncio.CancelledError:
        pass
