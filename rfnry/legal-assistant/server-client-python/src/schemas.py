from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Source(BaseModel):
    tool: str
    result_or_reason: str


class InvestigationReport(BaseModel):
    person: str | None = None
    summary: str
    sources: list[Source] = Field(default_factory=list)


class Classification(BaseModel):
    subject_kind: str
    subject_id: str
    skill: str
    specific_claims: list[str] = Field(default_factory=list)
    notes: str = ""


class PartyCheck(BaseModel):
    party_id: str
    status: Literal["clear", "opposing", "aligned", "ambiguous"]
    source: str = ""


class ConflictCheck(BaseModel):
    verdict: Literal["clear", "direct_conflict", "inconclusive"]
    parties_checked: list[PartyCheck] = Field(default_factory=list)
    notes: str = ""


class IntakeReport(BaseModel):
    decision: Literal["proceed", "decline", "needs_info"]
    classification: Classification
    conflict_check: ConflictCheck
    rationale: str


class FilingReview(BaseModel):
    filing_kind: str
    procedural_issues: list[str] = Field(default_factory=list)
    missing_exhibits: list[str] = Field(default_factory=list)
    citation_issues: list[str] = Field(default_factory=list)
    verdict: Literal["ready_to_file", "needs_revision", "block"]
