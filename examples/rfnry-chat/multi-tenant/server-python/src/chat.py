from __future__ import annotations

from rfnry_chat_protocol import Identity
from rfnry_chat_server import (
    ChatServer,
    ChatStore,
    HandlerContext,
    HandlerSend,
    MessageEvent,
)


async def _tenant_is_enough(identity: Identity, thread_id: str, action: str, *, target_id: str | None = None) -> bool:
    """Authorize policy: tenant match is sufficient — no per-thread membership required.

    The core server already checked `matches(thread.tenant, identity.tenant)` before
    authorize fires, so by the time we get here, the identity's tenant is compatible
    with the thread's tenant. In this "workspace is the room" model that's the full
    access decision; membership stays as a soft concept (for inbox invites, audit,
    recipient filtering) and is not an access gate.
    """
    del identity, thread_id, action, target_id
    return True


def create_chat_server(store: ChatStore) -> ChatServer:
    chat_server = ChatServer(store=store, authorize=_tenant_is_enough)

    @chat_server.on_message()
    async def log_message(ctx: HandlerContext, _send: HandlerSend) -> None:
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
