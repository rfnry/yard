from __future__ import annotations

from rfnry import Agent


async def run_resume(
    agent: Agent,
    *,
    session_id: str,
    scope: dict[str, str],
    task: str | None,
) -> str:
    return await agent.resume(
        session_id=session_id,
        scope=scope,
        task=task,
    )
