from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rfnry_chat_server import InMemoryChatStore

from src.agent import create_chat_client
from src.chat import create_chat_server

PORT = int(os.environ.get("PORT", "8000"))

chat_server = create_chat_server(store=InMemoryChatStore())
chat_client = create_chat_client(f"http://127.0.0.1:{PORT}")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    # Demonstrates the "consumer owns everything" pattern: both server and
    # client lifecycles are explicit sessions in the lifespan. No helper
    # is injecting anything. Consumer also owns include_router,
    # mount(), and uvicorn.run (see __main__ below).
    async with chat_server.running(), chat_client.running():
        print("chat server running (in-memory, no auth) + agent scheduled")
        yield


app = FastAPI(title="customer-support", lifespan=lifespan)
app.state.chat_server = chat_server
app.include_router(chat_server.router, prefix="/chat")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


asgi = chat_server.mount(app)


if __name__ == "__main__":
    import uvicorn

    try:
        uvicorn.run(asgi, host="0.0.0.0", port=PORT)
    except asyncio.CancelledError:
        pass
