from __future__ import annotations

from anthropic import AsyncAnthropic
from fastapi import FastAPI, Request
from rfnry_knowledge import MemoryEngine

from src import services
from src.providers import Settings
from src.schemas import ChatRequest, ChatResponse


def _engine(request: Request) -> MemoryEngine:
    return request.app.state.engine


def _chat_client(request: Request) -> AsyncAnthropic:
    return request.app.state.chat_client


def _settings(request: Request) -> Settings:
    return request.app.state.settings


def register(app: FastAPI) -> None:
    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/chat", response_model=ChatResponse)
    async def chat(req: ChatRequest, request: Request) -> ChatResponse:
        return await services.chat(
            engine=_engine(request),
            chat_client=_chat_client(request),
            memory_id=req.memory_id,
            message=req.message,
            settings=_settings(request),
        )
