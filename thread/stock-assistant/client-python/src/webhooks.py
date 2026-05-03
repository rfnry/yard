from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rfnry_chat_client import ChatClient
from rfnry_chat_protocol import TextPart, UserIdentity


class AlertUserRequest(BaseModel):
    user_id: str
    message: str
    user_name: str | None = None
    thread_id: str | None = None


def register(app: FastAPI, client: ChatClient) -> None:
    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/alert-user")
    async def alert_user(body: AlertUserRequest) -> dict[str, str]:
        if not body.user_id.strip():
            raise HTTPException(status_code=400, detail="user_id is required")
        user = UserIdentity(id=body.user_id, name=body.user_name or body.user_id)
        if body.thread_id is not None:
            async with client.send(body.thread_id) as send:
                event = await send.emit(
                    send.message([TextPart(text=body.message)], recipients=[user.id]),
                )
            thread_id = body.thread_id
        else:
            async with client.send_to(user) as send:
                event = await send.emit(
                    send.message([TextPart(text=body.message)], recipients=[user.id]),
                )
            thread_id = send.thread_id
        print(f"alerted user={body.user_id} thread={thread_id} event={event.id}")
        return {"thread_id": thread_id, "event_id": event.id}
