from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

import os  # noqa: E402
from collections.abc import AsyncGenerator  # noqa: E402
from contextlib import asynccontextmanager  # noqa: E402
from datetime import datetime  # noqa: E402

from fastapi import Depends, FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from rfnry_chat_protocol import Identity, Thread  # noqa: E402
from rfnry_chat_server import InMemoryChatStore  # noqa: E402
from rfnry_chat_server.server.rest.deps import identity_tenant, resolve_identity  # noqa: E402
from rfnry_chat_server.store.types import Page, ThreadCursor  # noqa: E402

from src.chat import bootstrap_channels, create_chat_server  # noqa: E402

PORT = int(os.environ.get("PORT", "8000"))

chat_server = create_chat_server(store=InMemoryChatStore())


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    await chat_server.start()
    await bootstrap_channels(chat_server.store)
    print("team-communication chat server running (in-memory, no auth)")
    try:
        yield
    finally:
        await chat_server.stop()


app = FastAPI(title="multi-tenant", lifespan=lifespan)
app.state.chat_server = chat_server


# Example-specific override: hide DM threads the caller isn't a member of.
#
# Background: channel threads declare `tenant = {"channel": <slug>}` and
# users/agents carry `tenant.channel = "*"`, so channels are visible via the
# library's tenant filter. DMs declare `tenant = {}`, which matches every
# caller at the tenant layer. Without this wrapper, every caller would see
# every DM listed in `GET /chat/threads` (even though `authorize` still
# prevents them from reading the events inside).
#
# MUST be registered BEFORE `app.include_router(chat_server.router, ...)` so
# FastAPI's first-match routing picks this handler over the library's one.
@app.get("/chat/threads", response_model=Page[Thread])
async def list_threads_with_dm_filter(
    limit: int = 50,
    cursor_created_at: str | None = None,
    cursor_id: str | None = None,
    identity: Identity = Depends(resolve_identity),
) -> Page[Thread]:
    cursor = None
    if cursor_created_at and cursor_id:
        cursor = ThreadCursor(
            created_at=datetime.fromisoformat(cursor_created_at),
            id=cursor_id,
        )
    page = await chat_server.store.list_threads(
        tenant_filter=identity_tenant(identity),
        cursor=cursor,
        limit=limit,
    )
    visible: list[Thread] = []
    for thread in page.items:
        kind = (thread.metadata or {}).get("kind")
        if kind == "dm" and not await chat_server.store.is_member(thread.id, identity.id):
            continue
        visible.append(thread)
    return Page[Thread](items=visible, next_cursor=page.next_cursor)


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
