from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

import os  # noqa: E402
from collections.abc import AsyncGenerator  # noqa: E402
from contextlib import asynccontextmanager  # noqa: E402

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from rfnry_chat_server import (  # noqa: E402
    ChatServer,
    HandlerContext,
    HandlerSend,
    InMemoryChatStore,
    MessageEvent,
)

PORT = int(os.environ.get("PORT", "8000"))


def create_chat_server() -> ChatServer:
    chat_server = ChatServer(store=InMemoryChatStore())

    @chat_server.on_message()
    async def log_message(ctx: HandlerContext, _send: HandlerSend) -> None:
        assert isinstance(ctx.event, MessageEvent)
        preview = next(
            (getattr(p, "text", "") for p in ctx.event.content if getattr(p, "type", None) == "text"),
            "",
        )
        print(f"msg thread={ctx.thread.id} author={ctx.event.author.id} preview={preview[:60]!r}")

    return chat_server


chat_server = create_chat_server()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    await chat_server.start()
    print("stock-assistant chat server running (in-memory, no auth)")
    try:
        yield
    finally:
        await chat_server.stop()


app = FastAPI(title="stock-assistant-server", lifespan=lifespan)
app.state.chat_server = chat_server
app.include_router(chat_server.router, prefix="/chat")
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


asgi = chat_server.mount_socketio(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(asgi, host="0.0.0.0", port=PORT)
