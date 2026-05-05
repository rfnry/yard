from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.engine import plan_trip, resume_plan


class PlanTripRequest(BaseModel):
    session_id: str
    traveler_id: str
    origin: str
    destination: str
    arrival_date: str
    departure_date: str
    travelers: int
    mood: str = "relaxing"
    budget_band: str = "mid-range"


class ResumePlanRequest(BaseModel):
    session_id: str
    traveler_id: str


def register(app: FastAPI) -> None:
    @app.post("/plan-trip")
    async def plan_route(req: PlanTripRequest) -> dict[str, object]:
        try:
            plan = await plan_trip(
                session_id=req.session_id,
                traveler_id=req.traveler_id,
                origin=req.origin,
                destination=req.destination,
                arrival_date=req.arrival_date,
                departure_date=req.departure_date,
                travelers=req.travelers,
                mood=req.mood,
                budget_band=req.budget_band,
            )
        except Exception as exc:
            raise HTTPException(500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {
            "session_id": req.session_id,
            "traveler_id": req.traveler_id,
            "plan": plan.model_dump(mode="json"),
        }

    @app.post("/plan-trip/resume")
    async def resume_route(req: ResumePlanRequest) -> dict[str, object]:
        try:
            plan = await resume_plan(
                session_id=req.session_id, traveler_id=req.traveler_id
            )
        except Exception as exc:
            raise HTTPException(500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {
            "session_id": req.session_id,
            "traveler_id": req.traveler_id,
            "plan": plan.model_dump(mode="json"),
        }
