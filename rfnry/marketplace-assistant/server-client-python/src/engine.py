from __future__ import annotations

import os

from anthropic import AsyncAnthropic
from rfnry import (
    AgentEngine,
    Observability,
    PrettyStderrSink,
    RefiningConfig,
    RefiningTasksConfig,
    SqliteTelemetrySink,
    Telemetry,
)

from src.provider import AnthropicProvider

agent_engine = AgentEngine(
    agents="../agents",
    provider=AnthropicProvider(
        client=AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"]),
        model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
    ),
    refining=RefiningConfig(methods=[RefiningTasksConfig(lookback=10)]),
    observability=Observability(sink=PrettyStderrSink()),
    telemetry=Telemetry(sink=SqliteTelemetrySink(agent_root="../agents")),
)


async def turn(session_id: str, message: str) -> str:
    result = await agent_engine.turn(session_id=session_id, message=message)
    return result


async def resume(session_id: str) -> str:
    result = await agent_engine.resume(session_id=session_id)
    return result
