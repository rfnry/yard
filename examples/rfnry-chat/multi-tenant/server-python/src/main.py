from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

import os  # noqa: E402
from collections.abc import AsyncGenerator  # noqa: E402
from contextlib import asynccontextmanager  # noqa: E402

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from rfnry_chat_server import InMemoryChatStore  # noqa: E402

from src.chat import create_chat_server  # noqa: E402

PORT = int(os.environ.get("PORT", "8000"))

chat_server = create_chat_server(store=InMemoryChatStore())


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    await chat_server.start()
    print("multi-tenant chat server running (in-memory, no auth)")
    try:
        yield
    finally:
        await chat_server.stop()


app = FastAPI(title="multi-tenant", lifespan=lifespan)
app.state.chat_server = chat_server
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
