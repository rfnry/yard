from __future__ import annotations

import asyncio
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import routes
from src.agent.server import AGENTS_ROOT, TEAM_NAME, WORKFLOW_NAME, engine

PORT = int(os.environ.get("PORT", "8102"))

app = FastAPI(title="rfnry-example-legal-assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.engine = engine
routes.register(app)


if __name__ == "__main__":
    print(f"legal-assistant agents root:  {AGENTS_ROOT}")
    print(f"legal-assistant team:         {TEAM_NAME}")
    print(f"legal-assistant workflow:     {WORKFLOW_NAME}")
    print(f"legal-assistant agents:       {engine.agent_names}")
    print(f"namespaces: case_id (single segment, validated by rfnry)")
    print(f"listening on http://0.0.0.0:{PORT}")
    try:
        uvicorn.run(app, host="0.0.0.0", port=PORT)
    except asyncio.CancelledError:
        pass
