from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rfnry_chat_client import ChatClient
from rfnry_chat_protocol import TextPart, UserIdentity

from src.agent import IDENTITY, register

CHAT_SERVER_URL = os.environ.get("CHAT_SERVER_URL", "http://127.0.0.1:8000")
PORT = int(os.environ.get("PORT", "9100"))


class AlertUserRequest(BaseModel):
    user_id: str
    message: str
    user_name: str | None = None
    thread_id: str | None = None


client = ChatClient(base_url=CHAT_SERVER_URL, identity=IDENTITY)
register(client)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    async with client.running():
        yield


app = FastAPI(title="stock-assistant-agent", lifespan=lifespan)
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


@app.post("/alert-user")
async def alert_user(body: AlertUserRequest) -> dict[str, str]:
    if not body.user_id.strip():
        raise HTTPException(status_code=400, detail="user_id is required")
    user = UserIdentity(id=body.user_id, name=body.user_name or body.user_id)
    thread, event = await client.open_thread_with(
        message=[TextPart(text=body.message)],
        invite=user,
        thread_id=body.thread_id,
    )
    print(f"alerted user={body.user_id} thread={thread.id} event={event.id}")
    return {"thread_id": thread.id, "event_id": event.id}


if __name__ == "__main__":
    import uvicorn

    print(f"stock-assistant agent connecting to {CHAT_SERVER_URL} as {IDENTITY.id}")
    try:
        uvicorn.run(app, host="0.0.0.0", port=PORT)
    except asyncio.CancelledError:
        pass
