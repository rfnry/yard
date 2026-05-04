from __future__ import annotations

from typing import Any

from rfnry import AgentEngine

from src.agent.schemas import CompetitorProfile, MarketScan, WeeklySummary
from src.agent.server import AGENT_NAME

_TASK_SCHEMAS: dict[str, type] = {
    "market-scan": MarketScan,
    "competitor-profile": CompetitorProfile,
    "weekly-summary": WeeklySummary,
}


async def run_turn(
    engine: AgentEngine,
    *,
    session_id: str,
    message: str,
    scope: dict[str, str],
    task: str | None,
) -> str | dict[str, Any]:
    schema = _TASK_SCHEMAS.get(task) if task is not None else None
    if schema is not None:
        result = await engine.turn(
            session_id=session_id,
            message=message,
            scope=scope,
            agent=AGENT_NAME,
            task=task,
            expect=schema,
        )
        return result.model_dump(mode="json")
    return await engine.turn(
        session_id=session_id,
        message=message,
        scope=scope,
        agent=AGENT_NAME,
        task=task,
    )
