from __future__ import annotations

from typing import Any

from rfnry import AgentEngine

from src.agent.schemas import InvestigationReport
from src.agent.server import RECORDS_AGENT, TEAM_NAME


async def run_turn(
    engine: AgentEngine,
    *,
    session_id: str,
    message: str,
    scope: dict[str, str],
    task: str | None,
) -> str | dict[str, Any]:
    if task == "investigate":
        report = await engine.turn(
            session_id=session_id,
            message=message,
            scope=scope,
            team=TEAM_NAME,
            agent=RECORDS_AGENT,
            task=task,
            expect=InvestigationReport,
        )
        return report.model_dump(mode="json")
    return await engine.turn(
        session_id=session_id,
        message=message,
        scope=scope,
        team=TEAM_NAME,
        agent=RECORDS_AGENT,
        task=task,
    )
