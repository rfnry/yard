from __future__ import annotations

from rfnry import AgentEngine, EditOutcome


async def run_optimize_skill(
    agent: AgentEngine,
    *,
    scope: dict[str, str],
    task: str,
    skill: str,
) -> list[EditOutcome]:
    return await agent.optimize_method(
        "skills",
        scope=scope,
        task=task,
        paths=[f"skills/{skill}.md"],
    )
