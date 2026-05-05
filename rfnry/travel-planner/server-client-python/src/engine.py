from __future__ import annotations

import os

from anthropic import AsyncAnthropic
from rfnry import (
    AgentEngine,
    Observability,
    OutputSchemas,
    PrettyStderrSink,
    RefiningConfig,
    RefiningTasksConfig,
    SqliteTelemetrySink,
    Telemetry,
)

from src.provider import AnthropicProvider
from src.schemas import (
    ActivityList,
    FlightOptions,
    HotelOptions,
    TripPlan,
    WeatherForecast,
)

WORKFLOW_NAME = "plan-trip"


def _provider_for(_member_name: str) -> AnthropicProvider:
    return AnthropicProvider(
        client=AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"]),
        model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
    )


agent_engine = AgentEngine(
    agents="../agents",
    provider=_provider_for,
    namespaces=["traveler_id"],
    output_schemas=OutputSchemas(
        tasks={
            "find-flights": FlightOptions,
            "find-hotels": HotelOptions,
            "curate-activities": ActivityList,
            "forecast": WeatherForecast,
            "synthesize-trip": TripPlan,
        },
        workflows={
            WORKFLOW_NAME: TripPlan,
        },
    ),
    refining=RefiningConfig(methods=[RefiningTasksConfig(lookback=10)]),
    observability=Observability(sink=PrettyStderrSink()),
    telemetry=Telemetry(sink=SqliteTelemetrySink(agent_root="../agents")),
)


async def plan_trip(
    *,
    session_id: str,
    traveler_id: str,
    origin: str,
    destination: str,
    arrival_date: str,
    departure_date: str,
    travelers: int,
    mood: str = "relaxing",
    budget_band: str = "mid-range",
) -> TripPlan:
    return await agent_engine.run_workflow(
        name=WORKFLOW_NAME,
        session_id=session_id,
        input={
            "origin": origin,
            "destination": destination,
            "arrival_date": arrival_date,
            "departure_date": departure_date,
            "travelers": travelers,
            "mood": mood,
            "budget_band": budget_band,
        },
        scope={"traveler_id": traveler_id},
        expect=TripPlan,
    )


async def resume_plan(*, session_id: str, traveler_id: str) -> TripPlan:
    return await agent_engine.resume_workflow(
        name=WORKFLOW_NAME,
        session_id=session_id,
        scope={"traveler_id": traveler_id},
        expect=TripPlan,
    )
