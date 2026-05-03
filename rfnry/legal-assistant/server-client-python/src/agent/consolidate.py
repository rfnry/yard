from __future__ import annotations

from rfnry import Agent, ConsolidationResult


async def run_consolidate(
    agent: Agent,
    *,
    scope: dict[str, str],
    task: str,
) -> ConsolidationResult:
    return await agent.consolidate(task=task, scope=scope)
