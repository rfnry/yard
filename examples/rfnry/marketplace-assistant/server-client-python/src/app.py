from __future__ import annotations

from pathlib import Path

from rfnry import Agent, RefiningConfig

from src.provider import build_provider

AGENT_ROOT: Path = Path(__file__).resolve().parent.parent / "agent"


def build_agent() -> Agent:
    return Agent(
        root=AGENT_ROOT,
        provider=build_provider(),
        namespaces=[],
        refining=RefiningConfig(default_lookback=10),
    )
