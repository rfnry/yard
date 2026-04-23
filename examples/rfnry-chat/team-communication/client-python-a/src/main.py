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

from src.agent import IDENTITY, register  # noqa: E402
from src.proactive import stream_proactive_message  # noqa: E402

CHAT_SERVER_URL = os.environ.get("CHAT_SERVER_URL", "http://127.0.0.1:8000")
PORT = int(os.environ.get("PORT", "9100"))


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


app = FastAPI(title="team-communication-agent-a", lifespan=lifespan)
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
    print(
        f"{IDENTITY.name} pinged channel={body.channel_id} "
        f"requested_by={body.requested_by.id} subject={subject!r}"
    )
    return {"ok": "true", "channel_id": body.channel_id, "subject": subject}


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
