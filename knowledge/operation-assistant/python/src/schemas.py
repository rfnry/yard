from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

SourceType = Literal["manual", "drawing"]


class QueryRequest(BaseModel):
    query: str
    knowledge_id: str | None = None


class SourceCitation(BaseModel):
    source_id: str
    page_number: int | None = None
    score: float


class QueryResponse(BaseModel):
    answer: str
    routing: str | None
    grounding: str | None
    sources: list[SourceCitation]


class IngestResponse(BaseModel):
    source_id: str
    source_type: SourceType
    chunk_count: int


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
