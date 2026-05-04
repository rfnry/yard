from __future__ import annotations

import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src import routes
from src.engine import agent_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.agent_engine = agent_engine
    yield


app = FastAPI(title="rfnry-example-analyst-assistant", lifespan=lifespan)
routes.register(app)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8102"))
    uvicorn.run(app, host="0.0.0.0", port=port)
