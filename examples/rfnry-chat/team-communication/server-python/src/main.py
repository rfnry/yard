from __future__ import annotations

import os
import secrets
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rfnry_chat_protocol import Identity, Thread, parse_identity
from rfnry_chat_server import InMemoryChatStore
from rfnry_chat_server.store.types import Page, ThreadCursor
from rfnry_chat_server.transport.rest.deps import identity_tenant, resolve_identity

from src.chat import bootstrap_channels, create_chat_server

PORT = int(os.environ.get("PORT", "8000"))

chat_server = create_chat_server(store=InMemoryChatStore(), data_root=Path("./var"))


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:

    await bootstrap_channels(chat_server.store)
    print("team-communication chat server running (in-memory, no auth)")
    yield


app = FastAPI(title="multi-tenant", lifespan=lifespan)
app.state.chat_server = chat_server


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


@app.post("/chat/dm", response_model=Thread)
async def find_or_create_dm(
    body: dict[str, Any] = Body(...),
    identity: Identity = Depends(resolve_identity),
) -> Thread:
    other_id_raw = body.get("with")
    if not isinstance(other_id_raw, str) or not other_id_raw.strip():
        raise HTTPException(status_code=400, detail="'with' is required (identity id)")
    other_id = other_id_raw.strip()
    is_self_dm = other_id == identity.id

    other_identity: Identity | None = None
    if not is_self_dm:
        raw_other = body.get("with_identity")
        if isinstance(raw_other, dict):
            try:
                other_identity = parse_identity(raw_other)
            except Exception as exc:  # noqa: BLE001
                raise HTTPException(status_code=400, detail=f"invalid with_identity: {exc}") from exc
            if other_identity.id != other_id:
                raise HTTPException(status_code=400, detail="with_identity.id must match 'with'")

    want_members: set[str] = {identity.id} if is_self_dm else {identity.id, other_id}

    page = await chat_server.store.list_threads(tenant_filter={}, limit=1000)
    for thread in page.items:
        kind = (thread.metadata or {}).get("kind")
        if kind != "dm":
            continue
        members = await chat_server.store.list_members(thread.id)
        if {m.identity_id for m in members} == want_members:
            if not await chat_server.store.is_member(thread.id, identity.id):
                await chat_server.store.add_member(thread.id, identity, added_by=identity)
            return thread

    if is_self_dm:
        client_id = f"selfdm_{identity.id}"
    else:
        client_id = "dm_" + "__".join(sorted([identity.id, other_id]))

    now = datetime.now(UTC)
    thread = Thread(
        id=f"th_{secrets.token_hex(8)}",
        tenant={},
        metadata={"kind": "dm"},
        created_at=now,
        updated_at=now,
    )
    created = await chat_server.store.create_thread(
        thread,
        caller_identity_id=identity.id,
        client_id=client_id,
    )
    await chat_server.store.add_member(created.id, identity, added_by=identity)
    if not is_self_dm and other_identity is not None:
        await chat_server.store.add_member(created.id, other_identity, added_by=identity)

    members = await chat_server.store.list_members(created.id)
    await chat_server.publish_thread_created(created)
    await chat_server.publish_members_updated(
        created.id,
        [m.identity for m in members],
        thread=created,
    )
    if not is_self_dm and other_identity is not None:
        await chat_server.publish_thread_invited(
            created,
            added_member=other_identity,
            added_by=identity,
        )
    return created


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
    chat_server.serve(app, host="0.0.0.0", port=PORT)
