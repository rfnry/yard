from __future__ import annotations

import os
from typing import Any

from anthropic import AsyncAnthropic
from rfnry import (
    AgentEngine,
    ConsolidationResult,
    Observability,
    OutputSchemas,
    PrettyStderrSink,
    RefiningConfig,
    RefiningTasksConfig,
    SqliteTelemetrySink,
    Telemetry,
)

from src.provider import AnthropicProvider
from src.schemas import CompetitorProfile, MarketScan, WeeklySummary

agent_engine = AgentEngine(
    agents="../agents",
    provider=AnthropicProvider(
        client=AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"]),
        model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
    ),
    namespaces=["client_id"],
    output_schemas=OutputSchemas(
        tasks={
            "market-scan": MarketScan,
            "competitor-profile": CompetitorProfile,
            "weekly-summary": WeeklySummary,
        },
    ),
    refining=RefiningConfig(methods=[RefiningTasksConfig(lookback=10)]),
    observability=Observability(sink=PrettyStderrSink()),
    telemetry=Telemetry(sink=SqliteTelemetrySink(agent_root="../agents")),
)

_TASK_SCHEMAS: dict[str, type] = {
    "market-scan": MarketScan,
    "competitor-profile": CompetitorProfile,
    "weekly-summary": WeeklySummary,
}


async def turn(
    session_id: str,
    client_id: str,
    message: str,
    task: str | None,
) -> str | dict[str, Any]:
    schema = _TASK_SCHEMAS.get(task) if task else None
    if schema is not None:
        report = await agent_engine.turn(
            session_id=session_id,
            message=message,
            scope={"client_id": client_id},
            task=task,
            expect=schema,
        )
        return report.model_dump(mode="json")
    return await agent_engine.turn(
        session_id=session_id,
        message=message,
        scope={"client_id": client_id},
        task=task,
    )


async def resume(session_id: str, client_id: str) -> str:
    result = await agent_engine.resume(
        session_id=session_id,
        scope={"client_id": client_id},
    )
    return result


async def consolidate(client_id: str, task: str) -> ConsolidationResult:
    runner = agent_engine.runner()
    return await runner.consolidate(task=task, scope={"client_id": client_id})
