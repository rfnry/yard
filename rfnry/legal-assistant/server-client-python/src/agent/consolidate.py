from __future__ import annotations

from rfnry import AgentEngine, ConsolidationResult

from src.agent.server import RECORDS_AGENT, TEAM_NAME


async def run_consolidate(
    engine: AgentEngine,
    *,
    scope: dict[str, str],
    task: str,
) -> ConsolidationResult:
    runner = engine.runner(team=TEAM_NAME, agent=RECORDS_AGENT)
    return await runner.consolidate(task=task, scope=scope)
