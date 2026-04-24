from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

import asyncio  # noqa: E402
import base64  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
from collections.abc import AsyncGenerator  # noqa: E402
from contextlib import asynccontextmanager  # noqa: E402

import httpx  # noqa: E402
from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from pydantic import BaseModel  # noqa: E402
from rfnry_chat_client import ChatClient  # noqa: E402
from rfnry_chat_protocol import Thread, UserIdentity  # noqa: E402

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


async def on_connect() -> None:
    await _join_all_channels()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    async with client.running(on_connect=on_connect):
        yield


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
    print(f"{IDENTITY.name} pinged channel={body.channel_id} requested_by={body.requested_by.id} subject={subject!r}")
    return {"ok": "true", "channel_id": body.channel_id, "subject": subject}


def _encode_identity_header(identity: UserIdentity | object) -> str:
    """Base64url-encode the agent's identity for the `x-rfnry-identity` header.

    Mirrors the default auth helper baked into ``ChatClient`` (see
    chat/packages/client-python .../client.py — `_default_auth`). The example
    server's `/chat/dm` endpoint reads this header via ``resolve_identity``.
    """
    raw = IDENTITY.model_dump(mode="json")
    return base64.urlsafe_b64encode(json.dumps(raw, separators=(",", ":")).encode("utf-8")).decode("ascii")


async def _find_or_create_dm(user: UserIdentity) -> Thread:
    """Call the example server's `/chat/dm` find-or-create endpoint.

    The library's `POST /chat/threads` dedups by `(caller_id, client_id)`,
    which creates a separate thread for each side of an agent+user DM (the
    bug this endpoint fixes). The server scans DM threads by member set and
    returns an existing match regardless of which side originally created it.
    """
    headers = {
        "content-type": "application/json",
        "x-rfnry-identity": _encode_identity_header(IDENTITY),
    }
    async with httpx.AsyncClient() as http:
        response = await http.post(
            f"{CHAT_SERVER_URL.rstrip('/')}/chat/dm",
            headers=headers,
            json={"with": user.id, "with_identity": user.model_dump(mode="json")},
        )
    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return Thread.model_validate(response.json())


class PingDirectBody(BaseModel):
    user_id: str
    user_name: str
    requested_by: RequestedBy


@app.post("/ping-direct")
async def ping_direct(body: PingDirectBody) -> dict[str, str]:
    user = UserIdentity(id=body.user_id, name=body.user_name, metadata={})

    # Find-or-create the DM via the example server's cross-caller-deduped
    # endpoint. Both the React sidebar (user clicking "Agent A") and this
    # webhook converge on the same thread for any given (agent, user) pair.
    thread = await _find_or_create_dm(user)
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
    import uvicorn

    print(f"{IDENTITY.name} connecting to {CHAT_SERVER_URL} as {IDENTITY.id}")
    try:
        uvicorn.run(app, host="0.0.0.0", port=PORT)
    except asyncio.CancelledError:
        pass
