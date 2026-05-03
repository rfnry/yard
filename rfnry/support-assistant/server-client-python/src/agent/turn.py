from __future__ import annotations

from rfnry import AgentEngine


async def run_turn(
    agent: AgentEngine,
    *,
    session_id: str,
    message: str,
    scope: dict[str, str],
    task: str | None,
) -> str:
    return await agent.turn(
        session_id=session_id,
        message=message,
        scope=scope,
        task=task,
    )
