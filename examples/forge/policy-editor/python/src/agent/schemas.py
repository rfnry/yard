from __future__ import annotations

from pydantic import BaseModel, Field


class ScribeStep(BaseModel):
    op: str
    target: str
    detail: str


class EditReport(BaseModel):
    policy_id: str
    request: str
    mode: str = "single"
    files_touched: list[str] = Field(default_factory=list)
    scribe_steps: list[ScribeStep] = Field(default_factory=list)
    audit_ids: list[str] = Field(default_factory=list)
    verify_failures: list[str] = Field(default_factory=list)
    summary: str
