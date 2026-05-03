from __future__ import annotations

from typing import Any

from rfnry import AgentEngine

from src.agent.schemas import InvestigationReport


async def run_turn(
    agent: AgentEngine,
    *,
    session_id: str,
    message: str,
    scope: dict[str, str],
    task: str | None,
) -> str | dict[str, Any]:
    if task == "investigate":
        report = await agent.turn(
            session_id=session_id,
            message=message,
            scope=scope,
            task=task,
            expect=InvestigationReport,
        )
        return report.model_dump(mode="json")
    return await agent.turn(
        session_id=session_id,
        message=message,
        scope=scope,
        task=task,
    )
