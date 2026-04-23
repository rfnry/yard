from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

import asyncio  # noqa: E402
import contextlib  # noqa: E402
import os  # noqa: E402
from collections.abc import AsyncGenerator  # noqa: E402
from contextlib import asynccontextmanager  # noqa: E402

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from pydantic import BaseModel  # noqa: E402
from rfnry_chat_client import ChatClient  # noqa: E402
from rfnry_chat_protocol import UserIdentity  # noqa: E402

from src.agent import IDENTITY, register  # noqa: E402
from src.proactive import stream_proactive_message  # noqa: E402

CHAT_SERVER_URL = os.environ.get("CHAT_SERVER_URL", "http://127.0.0.1:8000")
PORT = int(os.environ.get("PORT", "9102"))


client = ChatClient(base_url=CHAT_SERVER_URL, identity=IDENTITY)
register(client)

# Tracks threads this agent has already joined, so reconnect-driven discovery
# (on_connect → _join_all_channels) doesn't re-join threads that on_invited
# already picked up while the socket was live.
_joined_threads: set[str] = set()


async def _join_all_channels() -> None:
    """One-shot scan of tenant-visible threads at connect time.

    Filters to `metadata.kind == "channel"` — DMs are joined reactively via
    the on_invited handler when a user starts a DM with this agent. See
    ../../multi-tenant/client-python-a/src/main.py for the reconnect-recovery
    rationale.
    """
    page = await client.rest.list_threads()
    for thread in page["items"]:
        kind = (thread.metadata or {}).get("kind")
        if kind != "channel":
            continue
        if thread.id in _joined_threads:
            continue
        await client.join_thread(thread.id)
        _joined_threads.add(thread.id)
        print(f"{IDENTITY.name} joined channel thread={thread.id}")


@client.on_invited()
async def _on_invited(frame) -> None:  # type: ignore[no-untyped-def]
    _joined_threads.add(frame.thread.id)
    kind = (frame.thread.metadata or {}).get("kind")
    print(f"{IDENTITY.name} invited to thread={frame.thread.id} kind={kind}")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    async def on_connect() -> None:
        await _join_all_channels()

    agent_task = asyncio.create_task(client.run(on_connect=on_connect))
    print(f"{IDENTITY.name} connecting to {CHAT_SERVER_URL} as {IDENTITY.id}")
    try:
        yield
    finally:
        # Close the agent socket cleanly before cancelling the run loop.
        # See ../../customer-support/server-client-python/src/main.py for the
        # reasoning — avoids engineio cancelling its writer task mid-handshake
        # on SIGINT.
        with contextlib.suppress(BaseException):
            await client.disconnect()
        agent_task.cancel()
        try:
            await asyncio.wait_for(agent_task, timeout=5)
        except (TimeoutError, asyncio.CancelledError, Exception):
            pass


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


class RequestedBy(BaseModel):
    id: str
    name: str


class PingChannelBody(BaseModel):
    channel_id: str
    requested_by: RequestedBy


@app.post("/ping-channel")
async def ping_channel(body: PingChannelBody) -> dict[str, str]:
    subject = await stream_proactive_message(
        client,
        thread_id=body.channel_id,
        audience="channel",
        addressee_name=body.requested_by.name,
        mention_inline=True,
    )
    print(f"{IDENTITY.name} pinged channel={body.channel_id} requested_by={body.requested_by.id} subject={subject!r}")
    return {"ok": "true", "channel_id": body.channel_id, "subject": subject}


def _dm_client_id(a: str, b: str) -> str:
    """Stable per-caller client_id for a DM between two participants.

    ``client_id`` is how the server dedupes thread creations from the same
    caller (see packages/server-python .../rest/threads.py — repeated POSTs
    with the same ``client_id`` return the existing thread). Sorting the
    participant ids means agent-a + user-x always yields the same key, so
    repeated ``/ping-direct`` calls land in the same DM thread.
    """
    return "dm_" + "__".join(sorted([a, b]))


class PingDirectBody(BaseModel):
    user_id: str
    user_name: str
    requested_by: RequestedBy


@app.post("/ping-direct")
async def ping_direct(body: PingDirectBody) -> dict[str, str]:
    user = UserIdentity(id=body.user_id, name=body.user_name, metadata={})
    dm_key = _dm_client_id(IDENTITY.id, body.user_id)

    # Open-or-reuse the DM thread. ``open_thread_with`` always sends an
    # initial message, but here we want ``stream_proactive_message`` to post
    # the opener, so we drive the primitives directly:
    #   1. create_thread with a stable ``client_id`` — server returns the
    #      existing thread on the second call (idempotent per-caller).
    #   2. add_member for the user — ON CONFLICT DO NOTHING server-side.
    #   3. join_thread — idempotent; ensures we get live events.
    thread = await client.rest.create_thread(
        tenant={},
        metadata={"kind": "dm"},
        client_id=dm_key,
    )
    await client.add_member(thread.id, user)
    if thread.id not in _joined_threads:
        await client.join_thread(thread.id)
        _joined_threads.add(thread.id)

    subject = await stream_proactive_message(
        client,
        thread_id=thread.id,
        audience="direct DM",
        addressee_name=body.user_name,
        mention_inline=False,
    )
    print(f"{IDENTITY.name} pinged direct user={body.user_id} thread={thread.id} subject={subject!r}")
    return {"ok": "true", "thread_id": thread.id, "subject": subject}


if __name__ == "__main__":
    import signal

    import uvicorn

    # See customer-support/server-client-python/src/main.py for rationale —
    # take over signal handling so lifespan cleanup (await client.disconnect)
    # runs inside a non-cancelled task.
    config = uvicorn.Config(app, host="0.0.0.0", port=PORT)
    server = uvicorn.Server(config)
    server.install_signal_handlers = lambda: None  # type: ignore[attr-defined, method-assign]

    async def _serve() -> None:
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: setattr(server, "should_exit", True))
        await server.serve()

    asyncio.run(_serve())
