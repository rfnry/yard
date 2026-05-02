from __future__ import annotations

from typing import Any

from rfnry import Agent

from src.agent.schemas import EditReport


async def run_turn(
    agent: Agent,
    *,
    session_id: str,
    message: str,
    scope: dict[str, str],
) -> dict[str, Any]:
    report = await agent.turn(
        session_id=session_id,
        message=message,
        scope=scope,
        task="edit-policy",
        expect=EditReport,
    )
    return report.model_dump(mode="json")
