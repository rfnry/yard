from __future__ import annotations

import os
from pathlib import Path

from anthropic import AsyncAnthropic
from rfnry import Agent
from rfnry.providers.anthropic import AnthropicProvider
from rfnry_forge.scribe import ScribeConfig
from rfnry_forge.scribe.adapters.rfnry import scribe_tools

from src.agent.schemas import EditReport

AGENT_ROOT: Path = Path(__file__).resolve().parent.parent.parent / "agent"

scribe_tool_set = scribe_tools(
    ScribeConfig(
        commit_policy="strict",
        max_rewrite_size_chars=50_000,
    )
)

agent = Agent(
    root=AGENT_ROOT,
    provider=AnthropicProvider(
        client=AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"]),
        model=os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-7"),
    ),
    namespaces=["policy_id"],
    tools=scribe_tool_set,
    output_schemas={"EditReport": EditReport},
)
