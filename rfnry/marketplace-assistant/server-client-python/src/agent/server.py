from __future__ import annotations

import os
from pathlib import Path

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

from src.agent.provider import AnthropicProvider

AGENTS_ROOT: Path = Path(__file__).resolve().parent.parent.parent / "agents"
AGENT_NAME = "marketplace-assistant"

agent = AgentEngine(
    agents=AGENTS_ROOT,
    provider=AnthropicProvider(
        client=AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"]),
        model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
    ),
    refining=RefiningConfig(
        methods=[RefiningTasksConfig(lookback=10)],
    ),
    observability=Observability(sink=PrettyStderrSink()),
    telemetry=Telemetry(sink=SqliteTelemetrySink(agent_root=AGENTS_ROOT / AGENT_NAME)),
)
