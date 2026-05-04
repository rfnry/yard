from __future__ import annotations

import os
from typing import Any

from anthropic import AsyncAnthropic
from rfnry import (
    AgentEngine,
    ConsolidationResult,
    EditOutcome,
    GEPAOptimizeConfig,
    Observability,
    OutputSchemas,
    PrettyStderrSink,
    RefiningConfig,
    RefiningSkillsConfig,
    RefiningTasksConfig,
    SqliteTelemetrySink,
    Telemetry,
)

from src.provider import AnthropicProvider
from src.schemas import InvestigationReport

TEAM_NAME = "litigation-team"
LEADER_NAME = "case-strategist"
RECORDS_AGENT = "records-investigator"
WORKFLOW_NAME = "client-intake"


def _provider_for(_member_name: str) -> AnthropicProvider:
    return AnthropicProvider(
        client=AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"]),
        model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
    )


agent_engine = AgentEngine(
    agents="../agents",
    provider=_provider_for,
    namespaces=["case_id"],
    output_schemas=OutputSchemas(tasks={"investigate": InvestigationReport}),
    refining=RefiningConfig(
        methods=[
            RefiningTasksConfig(lookback=20),
            RefiningSkillsConfig(optimize=GEPAOptimizeConfig(budget="small")),
        ],
    ),
    observability=Observability(sink=PrettyStderrSink()),
    telemetry=Telemetry(sink=SqliteTelemetrySink(agent_root="../agents")),
)


async def turn(
    session_id: str,
    case_id: str,
    message: str,
    task: str | None,
) -> str | dict[str, Any]:
    if task == "investigate":
        report = await agent_engine.turn(
            session_id=session_id,
            message=message,
            scope={"case_id": case_id},
            team=TEAM_NAME,
            agent=RECORDS_AGENT,
            task=task,
            expect=InvestigationReport,
        )
        return report.model_dump(mode="json")
    return await agent_engine.turn(
        session_id=session_id,
        message=message,
        scope={"case_id": case_id},
        team=TEAM_NAME,
        agent=RECORDS_AGENT,
        task=task,
    )


async def resume(session_id: str, case_id: str) -> str:
    result = await agent_engine.resume(
        session_id=session_id,
        scope={"case_id": case_id},
    )
    return result


async def team_turn(session_id: str, case_id: str, message: str) -> str:
    result = await agent_engine.turn(
        session_id=session_id,
        message=message,
        scope={"case_id": case_id},
        team=TEAM_NAME,
    )
    return result


async def run_workflow(session_id: str, case_id: str, request: str) -> str:
    result = await agent_engine.run_workflow(
        name=WORKFLOW_NAME,
        session_id=session_id,
        input={"case_id": case_id, "request": request},
        scope={"case_id": case_id},
    )
    return result


async def resume_workflow(session_id: str, case_id: str) -> str:
    result = await agent_engine.resume_workflow(
        name=WORKFLOW_NAME,
        session_id=session_id,
        scope={"case_id": case_id},
    )
    return result


async def consolidate(case_id: str, task: str) -> ConsolidationResult:
    runner = agent_engine.runner(team=TEAM_NAME, agent=RECORDS_AGENT)
    return await runner.consolidate(task=task, scope={"case_id": case_id})


async def optimize_skill(case_id: str, task: str, skill: str) -> list[EditOutcome]:
    runner = agent_engine.runner(team=TEAM_NAME, agent=RECORDS_AGENT)
    return await runner.optimize_method(
        "skills",
        scope={"case_id": case_id},
        task=task,
        paths=[f"skills/{skill}.md"],
    )
