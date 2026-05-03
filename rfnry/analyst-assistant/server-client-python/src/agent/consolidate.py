from __future__ import annotations

from rfnry import AgentEngine, ConsolidationResult


async def run_consolidate(
    agent: AgentEngine,
    *,
    scope: dict[str, str],
    task: str,
) -> ConsolidationResult:
    return await agent.consolidate(task=task, scope=scope)
