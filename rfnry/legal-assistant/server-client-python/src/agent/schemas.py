from __future__ import annotations

from pydantic import BaseModel, Field


class Source(BaseModel):
    tool: str
    result_or_reason: str


class InvestigationReport(BaseModel):
    person: str | None = None
    summary: str
    sources: list[Source] = Field(default_factory=list)
