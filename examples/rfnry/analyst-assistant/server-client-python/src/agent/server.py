from __future__ import annotations

import os
from pathlib import Path

from anthropic import AsyncAnthropic
from rfnry import Agent, RefiningConfig, RefiningTasksConfig
from rfnry.providers.anthropic import AnthropicProvider

from src.agent.schemas import CompetitorProfile, MarketScan, WeeklySummary

AGENT_ROOT: Path = Path(__file__).resolve().parent.parent.parent / "agent"

agent = Agent(
    root=AGENT_ROOT,
    provider=AnthropicProvider(
        client=AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"]),
        model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
    ),
    namespaces=["client_id"],
    output_schemas={
        "MarketScan": MarketScan,
        "CompetitorProfile": CompetitorProfile,
        "WeeklySummary": WeeklySummary,
    },
    refining=RefiningConfig(
        methods=[RefiningTasksConfig(lookback=10)],
    ),
)
