from __future__ import annotations

from rfnry import AgentEngine, EditOutcome

from src.agent.server import RECORDS_AGENT, TEAM_NAME


async def run_optimize_skill(
    engine: AgentEngine,
    *,
    scope: dict[str, str],
    task: str,
    skill: str,
) -> list[EditOutcome]:
    runner = engine.runner(team=TEAM_NAME, agent=RECORDS_AGENT)
    return await runner.optimize_method(
        "skills",
        scope=scope,
        task=task,
        paths=[f"skills/{skill}.md"],
    )
