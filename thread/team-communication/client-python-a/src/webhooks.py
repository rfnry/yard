from __future__ import annotations

import base64
import json
import os

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rfnry_chat_client import ChatClient
from rfnry_chat_protocol import Thread, UserIdentity

from src.agent import IDENTITY
from src.proactive import stream_proactive_message

CHAT_SERVER_URL = os.environ.get("CHAT_SERVER_URL", "http://127.0.0.1:8000")


class RequestedBy(BaseModel):
    id: str
    name: str


class PingChannelBody(BaseModel):
    channel_id: str
    requested_by: RequestedBy


class PingDirectBody(BaseModel):
    user_id: str
    user_name: str
    requested_by: RequestedBy


def _encode_identity_header() -> str:
    raw = IDENTITY.model_dump(mode="json")
    return base64.urlsafe_b64encode(json.dumps(raw, separators=(",", ":")).encode("utf-8")).decode("ascii")


async def _find_or_create_dm(user: UserIdentity) -> Thread:
    headers = {
        "content-type": "application/json",
        "x-rfnry-identity": _encode_identity_header(),
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


def register(app: FastAPI, client: ChatClient) -> None:
    @app.post("/ping-channel")
    async def ping_channel(body: PingChannelBody) -> dict[str, str]:
        async with client.send(body.channel_id) as send:
            subject = await stream_proactive_message(
                send,
                audience="channel",
                addressee_name=body.requested_by.name,
                mention_inline=True,
                addressee_id=body.requested_by.id,
            )
        print(
            f"{IDENTITY.name} pinged channel={body.channel_id} requested_by={body.requested_by.id} subject={subject!r}"
        )
        return {"ok": "true", "channel_id": body.channel_id, "subject": subject}

    @app.post("/ping-direct")
    async def ping_direct(body: PingDirectBody) -> dict[str, str]:
        user = UserIdentity(id=body.user_id, name=body.user_name, metadata={})
        thread = await _find_or_create_dm(user)
        async with client.send_to(user, thread_id=thread.id) as send:
            subject = await stream_proactive_message(
                send,
                audience="direct DM",
                addressee_name=body.user_name,
                mention_inline=False,
                addressee_id=body.requested_by.id,
            )
        print(f"{IDENTITY.name} pinged direct user={body.user_id} thread={thread.id} subject={subject!r}")
        return {"ok": "true", "thread_id": thread.id, "subject": subject}
