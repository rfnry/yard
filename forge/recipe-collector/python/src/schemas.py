from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

SourceType = Literal["recipe"]


class QueryRequest(BaseModel):
    query: str
    knowledge_id: str | None = None


class SourceCitation(BaseModel):
    source_id: str
    page_number: int | None = None
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceCitation]


class IngestResponse(BaseModel):
    source_id: str
    chunk_count: int


class VerifyRequest(BaseModel):
    source_id: str
    raw_path: str
    knowledge_id: str | None = None


class CountDelta(BaseModel):
    counts_before: dict[str, int]
    counts_after: dict[str, int]


class FidelityReport(BaseModel):
    source_id: str
    raw_path: str
    parser_used: str
    similarity: float
    deletion_paths: list[str]
    corruption_paths: list[dict]
    count_delta: CountDelta
    notes: str
