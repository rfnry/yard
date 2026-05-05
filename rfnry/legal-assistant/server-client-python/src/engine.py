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
from src.schemas import (
    ConflictCheck,
    FilingReview,
    IntakeReport,
    InvestigationReport,
)

INTAKE_TEAM = "intake-team"
LITIGATION_TEAM = "litigation-team"
RECORDS_AGENT = "records-investigator"
WORKFLOW_NAME = "open-matter"


def _provider_for(_member_name: str) -> AnthropicProvider:
    return AnthropicProvider(
        client=AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"]),
        model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
    )


agent_engine = AgentEngine(
    agents="../agents",
    provider=_provider_for,
    namespaces=["case_id"],
    output_schemas=OutputSchemas(
        tasks={
            "investigate": InvestigationReport,
            "triage": IntakeReport,
            "check-conflicts": ConflictCheck,
            "review-filing": FilingReview,
        },
    ),
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
            team=LITIGATION_TEAM,
            agent=RECORDS_AGENT,
            task=task,
            expect=InvestigationReport,
        )
        return report.model_dump(mode="json")
    return await agent_engine.turn(
        session_id=session_id,
        message=message,
        scope={"case_id": case_id},
        team=LITIGATION_TEAM,
        agent=RECORDS_AGENT,
        task=task,
    )


async def resume(session_id: str, case_id: str) -> str:
    return await agent_engine.resume(
        session_id=session_id,
        scope={"case_id": case_id},
    )


async def intake_turn(session_id: str, case_id: str, message: str) -> str:
    return await agent_engine.turn(
        session_id=session_id,
        message=message,
        scope={"case_id": case_id},
        team=INTAKE_TEAM,
    )


async def litigation_turn(session_id: str, case_id: str, message: str) -> str:
    return await agent_engine.turn(
        session_id=session_id,
        message=message,
        scope={"case_id": case_id},
        team=LITIGATION_TEAM,
    )


async def run_workflow(
    session_id: str, case_id: str, client_name: str, matter_summary: str
) -> str:
    return await agent_engine.run_workflow(
        name=WORKFLOW_NAME,
        session_id=session_id,
        input={
            "case_id": case_id,
            "client_name": client_name,
            "matter_summary": matter_summary,
        },
        scope={"case_id": case_id},
    )


async def resume_workflow(session_id: str, case_id: str) -> str:
    return await agent_engine.resume_workflow(
        name=WORKFLOW_NAME,
        session_id=session_id,
        scope={"case_id": case_id},
    )


async def consolidate(case_id: str, task: str) -> ConsolidationResult:
    runner = agent_engine.runner(team=LITIGATION_TEAM, agent=RECORDS_AGENT)
    return await runner.consolidate(task=task, scope={"case_id": case_id})


async def optimize_skill(case_id: str, task: str, skill: str) -> list[EditOutcome]:
    runner = agent_engine.runner(team=LITIGATION_TEAM, agent=RECORDS_AGENT)
    return await runner.optimize_method(
        "skills",
        scope={"case_id": case_id},
        task=task,
        paths=[f"skills/{skill}.md"],
    )
