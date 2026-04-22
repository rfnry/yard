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
from rfnry_chat_server import InMemoryChatStore  # noqa: E402

from src.agent import create_chat_client  # noqa: E402
from src.chat import create_chat_server  # noqa: E402

PORT = int(os.environ.get("PORT", "8000"))

chat_server = create_chat_server(store=InMemoryChatStore())


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    await chat_server.start()
    print("chat server running (in-memory, no auth)")

    chat_client = create_chat_client(f"http://127.0.0.1:{PORT}")
    agent_task = asyncio.create_task(chat_client.run())
    print("agent scheduled")

    try:
        yield
    finally:
        with contextlib.suppress(BaseException):
            await chat_client.disconnect()
        agent_task.cancel()
        try:
            await asyncio.wait_for(agent_task, timeout=5)
        except (TimeoutError, asyncio.CancelledError, Exception):
            pass
        await chat_server.stop()


app = FastAPI(title="customer-support", lifespan=lifespan)
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
    import signal

    import uvicorn

    # Take over signal handling instead of letting uvicorn cancel the main
    # task on SIGINT. Flipping `should_exit = True` lets uvicorn exit its
    # main loop through the normal shutdown path — our lifespan `finally`
    # block then runs inside a *non-cancelled* task, so `await
    # chat_client.disconnect()` can complete its engineio handshake cleanly
    # instead of having CancelledError propagate into socketio-client's
    # internal writer tasks.
    config = uvicorn.Config(asgi, host="0.0.0.0", port=PORT)
    server = uvicorn.Server(config)
    server.install_signal_handlers = lambda: None  # type: ignore[attr-defined, method-assign]

    async def _serve() -> None:
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: setattr(server, "should_exit", True))
        await server.serve()

    asyncio.run(_serve())
