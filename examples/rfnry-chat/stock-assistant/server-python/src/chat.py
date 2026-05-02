from __future__ import annotations

from pathlib import Path

from rfnry_chat_server import (
    ChatServer,
    ChatStore,
    HandlerContext,
    MessageEvent,
    Send,
)


def create_chat_server(*, store: ChatStore, data_root: Path | None = None) -> ChatServer:
    chat_server = ChatServer(store=store, data_root=data_root)

    @chat_server.on_message()
    async def log_message(ctx: HandlerContext, _send: Send) -> None:
        assert isinstance(ctx.event, MessageEvent)
        preview = next(
            (getattr(p, "text", "") for p in ctx.event.content if getattr(p, "type", None) == "text"),
            "",
        )
        print(f"msg thread={ctx.thread.id} author={ctx.event.author.id} preview={preview[:60]!r}")

    return chat_server
