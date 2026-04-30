from __future__ import annotations

import asyncio
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rfnry import Agent, RefiningConfig
from src import routes
from src.provider import build_provider

PORT = int(os.environ.get("PORT", "8103"))
AGENT_ROOT = Path(__file__).resolve().parent.parent / "agent"

agent = Agent(
    root=AGENT_ROOT,
    provider=build_provider(),
    namespaces=[],
    refining=RefiningConfig(default_lookback=10),
)

app = FastAPI(title="rfnry-example-stock-assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.agent = agent
routes.register(app)


if __name__ == "__main__":
    print(f"stock-assistant agent root: {AGENT_ROOT}")
    print(f"listening on http://0.0.0.0:{PORT}")
    print(f"stub upstream: http://0.0.0.0:{PORT}/quote/<ticker>")
    try:
        uvicorn.run(app, host="0.0.0.0", port=PORT)
    except asyncio.CancelledError:
        pass
