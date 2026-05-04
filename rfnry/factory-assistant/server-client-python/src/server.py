from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src import routes
from src.engine import build_engine
from src.knowledge_engine import build_engine as build_knowledge
from src.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = Settings.from_env()
    knowledge = build_knowledge(settings)
    async with knowledge:
        agent_engine = build_engine(settings, knowledge)
        app.state.settings = settings
        app.state.knowledge = knowledge
        app.state.agent_engine = agent_engine
        yield


app = FastAPI(title="rfnry-example-factory-assistant", lifespan=lifespan)
routes.register(app)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8301"))
    uvicorn.run(app, host="0.0.0.0", port=port)
