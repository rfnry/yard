from __future__ import annotations

import os
from pathlib import Path

from anthropic import AsyncAnthropic
from rfnry import (
    Agent,
    GEPAOptimizeConfig,
    Observability,
    PrettyStderrSink,
    RefiningConfig,
    RefiningSkillsConfig,
    RefiningTasksConfig,
    SqliteTelemetrySink,
    Telemetry,
)
from rfnry.providers.anthropic import AnthropicProvider

from src.agent.schemas import InvestigationReport

AGENT_ROOT: Path = Path(__file__).resolve().parent.parent.parent / "agent"

agent = Agent(
    root=AGENT_ROOT,
    provider=AnthropicProvider(
        client=AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"]),
        model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
    ),
    namespaces=["case_id"],
    output_schemas={"InvestigationReport": InvestigationReport},
    refining=RefiningConfig(
        methods=[
            RefiningTasksConfig(lookback=20),
            RefiningSkillsConfig(optimize=GEPAOptimizeConfig(budget="small")),
        ],
    ),
    observability=Observability(sink=PrettyStderrSink()),
    telemetry=Telemetry(sink=SqliteTelemetrySink(agent_root=AGENT_ROOT)),
)
