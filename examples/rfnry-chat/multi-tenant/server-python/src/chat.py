from __future__ import annotations

from pathlib import Path

from rfnry_chat_protocol import Identity
from rfnry_chat_server import (
    ChatServer,
    ChatStore,
    HandlerContext,
    MessageEvent,
    Send,
)


async def _tenant_is_enough(identity: Identity, thread_id: str, action: str, *, target_id: str | None = None) -> bool:

    del identity, thread_id, action, target_id
    return True


def create_chat_server(store: ChatStore, *, data_root: Path | None = None) -> ChatServer:
    chat_server = ChatServer(store=store, authorize=_tenant_is_enough, data_root=data_root)

    @chat_server.on_message()
    async def log_message(ctx: HandlerContext, _send: Send) -> None:
        assert isinstance(ctx.event, MessageEvent)
        preview = next(
            (getattr(p, "text", "") for p in ctx.event.content if getattr(p, "type", None) == "text"),
            "",
        )
        print(
            f"msg thread={ctx.thread.id} tenant={ctx.thread.tenant} "
            f"author={ctx.event.author.id} preview={preview[:60]!r}"
        )

    return chat_server
