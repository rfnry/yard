from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rfnry_chat_server import (
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

app = FastAPI(title="stock-assistant-server")
app.state.chat_server = chat_server
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


if __name__ == "__main__":
    print("stock-assistant chat server running (in-memory, no auth)")
    chat_server.serve(app, host="0.0.0.0", port=PORT)
