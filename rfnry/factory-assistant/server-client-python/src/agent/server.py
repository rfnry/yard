from __future__ import annotations

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
from rfnry_knowledge import KnowledgeEngine

from src.agent.executors import build_knowledge_executor
from src.agent.provider import AnthropicProvider
from src.settings import Settings

AGENTS_ROOT: Path = Path(__file__).resolve().parent.parent.parent / "agents"
AGENT_NAME = "factory-assistant"


def build_agent(settings: Settings, knowledge: KnowledgeEngine) -> AgentEngine:
    return AgentEngine(
        agents=AGENTS_ROOT,
        provider=AnthropicProvider(
            client=AsyncAnthropic(api_key=settings.anthropic_api_key),
            model=settings.anthropic_model,
        ),
        executors={
            "knowledge_query": build_knowledge_executor(knowledge, settings),
        },
        refining=RefiningConfig(
            methods=[RefiningTasksConfig(lookback=10)],
        ),
        observability=Observability(sink=PrettyStderrSink()),
        telemetry=Telemetry(sink=SqliteTelemetrySink(agent_root=AGENTS_ROOT / AGENT_NAME)),
    )
