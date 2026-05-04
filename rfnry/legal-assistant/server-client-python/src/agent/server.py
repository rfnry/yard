from __future__ import annotations

import os
from pathlib import Path

from anthropic import AsyncAnthropic
from rfnry import (
    AgentEngine,
    GEPAOptimizeConfig,
    Observability,
    PrettyStderrSink,
    RefiningConfig,
    RefiningSkillsConfig,
    RefiningTasksConfig,
    SqliteTelemetrySink,
    Telemetry,
)

from src.agent.provider import AnthropicProvider
from src.agent.schemas import InvestigationReport

AGENTS_ROOT: Path = Path(__file__).resolve().parent.parent.parent / "agents"
TEAM_NAME = "litigation-team"
LEADER_NAME = "case-strategist"
RECORDS_AGENT = "records-investigator"
WORKFLOW_NAME = "client-intake"


def _provider_for(_member_name: str) -> AnthropicProvider:
    return AnthropicProvider(
        client=AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"]),
        model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
    )


engine = AgentEngine(
    agents=AGENTS_ROOT,
    provider=_provider_for,
    namespaces=["case_id"],
    output_schemas={"InvestigationReport": InvestigationReport},
    refining=RefiningConfig(
        methods=[
            RefiningTasksConfig(lookback=20),
            RefiningSkillsConfig(optimize=GEPAOptimizeConfig(budget="small")),
        ],
    ),
    observability=Observability(sink=PrettyStderrSink()),
    telemetry=Telemetry(
        sink=SqliteTelemetrySink(agent_root=AGENTS_ROOT / TEAM_NAME)
    ),
)
