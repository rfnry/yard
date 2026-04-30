from __future__ import annotations

import asyncio
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import routes
from src.app import AGENT_ROOT, build_agent

PORT = int(os.environ.get("PORT", "8102"))

app = FastAPI(title="rfnry-example-legal-assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.agent = build_agent()
routes.register(app)


if __name__ == "__main__":
    print(f"legal-assistant agent root: {AGENT_ROOT}")
    print(f"namespaces: case_id (single segment, validated by rfnry)")
    print(f"listening on http://0.0.0.0:{PORT}")
    try:
        uvicorn.run(app, host="0.0.0.0", port=PORT)
    except asyncio.CancelledError:
        pass
