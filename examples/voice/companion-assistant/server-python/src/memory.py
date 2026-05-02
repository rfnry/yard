from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class CompanionTurn(BaseModel):
    model_config = ConfigDict(frozen=True)
    speaker_id: Literal["user", "agent"]
    text: str
    timestamp_ms: int = 0


class CompanionContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    summary: str
    recent_turns: list[CompanionTurn]


class CompanionMemory:
    def __init__(self, *, max_turns: int = 20) -> None:
        self._max_turns = max_turns
        self._turns: dict[str, list[CompanionTurn]] = {}
        self._summaries: dict[str, str] = {}

    def get(self, user_name: str) -> CompanionContext:
        return CompanionContext(
            name=user_name,
            summary=self._summaries.get(user_name, ""),
            recent_turns=list(self._turns.get(user_name, [])),
        )

    def append(
        self,
        user_name: str,
        *,
        speaker: Literal["user", "agent"],
        text: str,
        timestamp_ms: int = 0,
    ) -> None:
        bucket = self._turns.setdefault(user_name, [])
        bucket.append(CompanionTurn(speaker_id=speaker, text=text, timestamp_ms=timestamp_ms))
        if len(bucket) > self._max_turns:
            del bucket[0 : len(bucket) - self._max_turns]

    def set_summary(self, user_name: str, summary: str) -> None:
        self._summaries[user_name] = summary

    def reset(self, user_name: str) -> None:
        self._turns.pop(user_name, None)
        self._summaries.pop(user_name, None)
