from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import routes
from src.rag import lifespan_engine

PORT = int(os.environ.get("PORT", "8201"))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with lifespan_engine() as rag:
        app.state.rag = rag
        yield


app = FastAPI(title="rfnry-rag-example-operation-assistant", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
routes.register(app)


if __name__ == "__main__":
    print(f"operation-assistant listening on http://0.0.0.0:{PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
