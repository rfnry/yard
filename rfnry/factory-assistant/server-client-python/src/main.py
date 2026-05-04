from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import routes
from src.agent.server import AGENTS_ROOT, build_agent
from src.knowledge_engine import build_engine
from src.settings import Settings

PORT = int(os.environ.get("PORT", "8301"))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = Settings.from_env()
    knowledge = build_engine(settings)
    async with knowledge:
        agent = build_agent(settings, knowledge)
        app.state.settings = settings
        app.state.knowledge = knowledge
        app.state.agent = agent
        yield


app = FastAPI(title="rfnry-example-factory-assistant", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
routes.register(app)


if __name__ == "__main__":
    print(f"factory-assistant agent root: {AGENTS_ROOT}")
    print(f"listening on http://0.0.0.0:{PORT}")
    try:
        uvicorn.run(app, host="0.0.0.0", port=PORT)
    except asyncio.CancelledError:
        pass
