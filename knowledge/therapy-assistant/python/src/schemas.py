from __future__ import annotations

from pydantic import BaseModel


class ChatRequest(BaseModel):
    memory_id: str
    message: str


class RecalledMemory(BaseModel):
    text: str
    score: float


class ChatResponse(BaseModel):
    reply: str
    recalled: list[RecalledMemory]
