from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import routes
from src.engine import lifespan_engine
from src.providers import Settings, chat_client

PORT = int(os.environ.get("PORT", "8202"))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = Settings.from_env()
    app.state.settings = settings
    app.state.chat_client = chat_client(settings)
    async with lifespan_engine() as engine:
        app.state.engine = engine
        yield


app = FastAPI(title="rfnry-knowledge-example-therapy-assistant", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
routes.register(app)


if __name__ == "__main__":
    print(f"therapy-assistant listening on http://0.0.0.0:{PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
