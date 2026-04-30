from __future__ import annotations

import os
from pathlib import Path

from anthropic import AsyncAnthropic
from rfnry import Agent, RefiningConfig
from rfnry.providers.anthropic import AnthropicProvider

AGENT_ROOT: Path = Path(__file__).resolve().parent.parent / "agent"


def build_agent() -> Agent:
    provider = AnthropicProvider(
        client=AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"]),
        model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
    )
    return Agent(
        root=AGENT_ROOT,
        provider=provider,
        namespaces=["case_id"],
        refining=RefiningConfig(
            default_lookback=20,
            use_sqlite_lessons=True,
            use_sqlite_reflections=True,
            use_sqlite_consolidations=True,
        ),
    )
