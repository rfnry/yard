from __future__ import annotations

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

from src.executors import build_knowledge_executor
from src.provider import AnthropicProvider
from src.settings import Settings


def build_engine(settings: Settings, knowledge: KnowledgeEngine) -> AgentEngine:
    return AgentEngine(
        agents="../agents",
        provider=AnthropicProvider(
            client=AsyncAnthropic(api_key=settings.anthropic_api_key),
            model=settings.anthropic_model,
        ),
        executors={
            "knowledge_query": build_knowledge_executor(knowledge, settings),
        },
        refining=RefiningConfig(methods=[RefiningTasksConfig(lookback=10)]),
        observability=Observability(sink=PrettyStderrSink()),
        telemetry=Telemetry(sink=SqliteTelemetrySink(agent_root="../agents")),
    )


async def turn(agent_engine: AgentEngine, session_id: str, message: str) -> str:
    result = await agent_engine.turn(
        session_id=session_id,
        message=message,
        task="assist-technician",
    )
    return result


async def resume(agent_engine: AgentEngine, session_id: str) -> str:
    result = await agent_engine.resume(session_id=session_id)
    return result
