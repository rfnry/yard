from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

SourceType = Literal["manual", "drawing", "transcript"]


class MessageRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    thread_id: str
    reply: str


class IngestResponse(BaseModel):
    source_id: str
    source_type: SourceType
    chunk_count: int


class SourceCitation(BaseModel):
    source_id: str
    page_number: int | None = None
    score: float


class SourceInfo(BaseModel):
    source_id: str
    source_type: str | None
    chunk_count: int
    tags: list[str]


class KnowledgeListResponse(BaseModel):
    knowledge_id: str
    sources: list[SourceInfo]
    total_chunks: int
    estimated_tokens: int | None
