from __future__ import annotations

from rfnry import AgentEngine

from src.agent.server import AGENT_NAME


async def run_turn(
    engine: AgentEngine,
    *,
    session_id: str,
    message: str,
    scope: dict[str, str],
    task: str | None,
) -> str:
    return await engine.turn(
        session_id=session_id,
        message=message,
        scope=scope,
        agent=AGENT_NAME,
        task=task,
    )
