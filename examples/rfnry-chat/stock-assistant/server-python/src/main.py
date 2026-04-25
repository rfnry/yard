from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rfnry_chat_server import InMemoryChatStore

from src import routes
from src.chat import create_chat_server

PORT = int(os.environ.get("PORT", "8000"))

chat_server = create_chat_server(store=InMemoryChatStore())

app = FastAPI(title="stock-assistant-server")
app.state.chat_server = chat_server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
routes.register(app)


if __name__ == "__main__":
    print("stock-assistant chat server running (in-memory, no auth)")
    chat_server.serve(app, host="0.0.0.0", port=PORT)
