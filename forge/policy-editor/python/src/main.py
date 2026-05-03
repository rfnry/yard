from __future__ import annotations

import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import routes
from src.agent.server import AGENT_ROOT, agent

PORT = int(os.environ.get("PORT", "8104"))

app = FastAPI(title="rfnry-example-policy-editor")
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
    print(f"policy-editor agent root: {AGENT_ROOT}")
    print("namespaces: policy_id (single segment, validated by rfnry)")
    print(f"listening on http://0.0.0.0:{PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
