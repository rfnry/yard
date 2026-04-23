from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

import os  # noqa: E402
import secrets  # noqa: E402
from collections.abc import AsyncGenerator  # noqa: E402
from contextlib import asynccontextmanager  # noqa: E402
from datetime import UTC, datetime  # noqa: E402
from typing import Any  # noqa: E402

from fastapi import Body, Depends, FastAPI, HTTPException  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from rfnry_chat_protocol import Identity, Thread, parse_identity  # noqa: E402
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


# Example-specific endpoint: find-or-create a DM thread with deduplication that
# works ACROSS callers.
#
# Background: the library's `POST /chat/threads` dedups by `(caller_id,
# client_id)` — two different callers passing the same `client_id` each get
# their own thread. For DMs that's a bug: when agent-a's webhook creates a DM
# with user u_xyz, and u_xyz later clicks "Agent A" in the sidebar, both ends
# need to land on the SAME thread. We solve that here by scanning existing DM
# threads and matching on the member set, not on the per-caller client_id.
#
# Body shape: `{"with": "<identity_id>", "with_identity": {role, id, name,
# metadata}}`. The `with_identity` blob is required so we can add the other
# side as a member when creating a fresh thread — the server otherwise has no
# way to reconstruct the remote identity's role/metadata. For self-DMs
# (`with == identity.id`), `with_identity` is ignored.
#
# MUST be registered BEFORE `app.include_router(...)` so our handler wins over
# anything the library might add later under the same path.
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

    # Expected participant set for matching — single-element for self-DMs.
    want_members: set[str] = {identity.id} if is_self_dm else {identity.id, other_id}

    # Scan every DM thread (visible at the library's tenant layer, which is
    # permissive for `tenant={}` DMs) and return the first one whose member
    # set equals the expected pair. Not bounded by caller — cross-caller dedup
    # is exactly what we're fixing.
    page = await chat_server.store.list_threads(tenant_filter={}, limit=1000)
    for thread in page.items:
        kind = (thread.metadata or {}).get("kind")
        if kind != "dm":
            continue
        members = await chat_server.store.list_members(thread.id)
        if {m.identity_id for m in members} == want_members:
            # Found a match. Ensure caller is a member (should always be true,
            # but guard against stale state) and return.
            if not await chat_server.store.is_member(thread.id, identity.id):
                await chat_server.store.add_member(thread.id, identity, added_by=identity)
            return thread

    # No existing thread — mint one. `client_id` is still recorded on the
    # caller side for consistency with other code paths; matching is via the
    # member set above, so the per-caller key is purely informational.
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
    # Publish the frames the library would normally publish — so both sides
    # receive `thread:created`, `members:updated`, and `thread:invited` in
    # real time (mirrors what POST /chat/threads + POST /members does).
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
