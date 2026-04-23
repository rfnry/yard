from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

import asyncio  # noqa: E402
import contextlib  # noqa: E402
import os  # noqa: E402
from collections.abc import AsyncGenerator  # noqa: E402
from contextlib import asynccontextmanager  # noqa: E402

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from pydantic import BaseModel  # noqa: E402
from rfnry_chat_client import ChatClient  # noqa: E402
from rfnry_chat_protocol import TextPart, UserIdentity  # noqa: E402

from src.agent import IDENTITY, register  # noqa: E402

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
    agent_task = asyncio.create_task(client.run())
    print(f"stock-assistant agent connecting to {CHAT_SERVER_URL} as {IDENTITY.id}")
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
