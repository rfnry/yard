from __future__ import annotations

import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.routes as routes
import src.ws as ws
from src.manager import SessionManager

PORT = int(os.environ.get("PORT", "8301"))

app = FastAPI(title="rfnry-voice-example-support-assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.manager = SessionManager()
routes.register(app)
ws.register(app)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    print(f"support-assistant listening on http://0.0.0.0:{PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
