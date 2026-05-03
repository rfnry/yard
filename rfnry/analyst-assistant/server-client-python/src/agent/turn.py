from __future__ import annotations

from typing import Any

from rfnry import AgentEngine

from src.agent.schemas import CompetitorProfile, MarketScan, WeeklySummary

_TASK_SCHEMAS: dict[str, type] = {
    "market-scan": MarketScan,
    "competitor-profile": CompetitorProfile,
    "weekly-summary": WeeklySummary,
}


async def run_turn(
    agent: AgentEngine,
    *,
    session_id: str,
    message: str,
    scope: dict[str, str],
    task: str | None,
) -> str | dict[str, Any]:
    schema = _TASK_SCHEMAS.get(task) if task is not None else None
    if schema is not None:
        result = await agent.turn(
            session_id=session_id,
            message=message,
            scope=scope,
            task=task,
            expect=schema,
        )
        return result.model_dump(mode="json")
    return await agent.turn(
        session_id=session_id,
        message=message,
        scope=scope,
        task=task,
    )
