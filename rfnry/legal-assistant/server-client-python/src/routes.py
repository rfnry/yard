from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.engine import (
    INTAKE_TEAM,
    LITIGATION_TEAM,
    agent_engine,
    consolidate,
    intake_turn,
    litigation_turn,
    optimize_skill,
    resume,
    resume_workflow,
    run_workflow,
    turn,
)


class TurnRequest(BaseModel):
    session_id: str
    case_id: str
    message: str
    task: str | None = "investigate"


class ResumeRequest(BaseModel):
    session_id: str
    case_id: str


class ConsolidateRequest(BaseModel):
    case_id: str
    task: str = "investigate"


class OptimizeSkillRequest(BaseModel):
    case_id: str
    skill: str
    task: str = "investigate"


class TeamTurnRequest(BaseModel):
    session_id: str
    case_id: str
    message: str


class WorkflowRunRequest(BaseModel):
    session_id: str
    case_id: str
    client_name: str
    matter_summary: str


class WorkflowResumeRequest(BaseModel):
    session_id: str
    case_id: str


def register(app: FastAPI) -> None:
    @app.post("/turn")
    async def turn_route(req: TurnRequest) -> dict[str, object]:
        try:
            reply = await turn(req.session_id, req.case_id, req.message, req.task)
        except Exception as exc:
            raise HTTPException(500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {"session_id": req.session_id, "case_id": req.case_id, "reply": reply}

    @app.post("/resume")
    async def resume_route(req: ResumeRequest) -> dict[str, object]:
        reply = await resume(req.session_id, req.case_id)
        return {"session_id": req.session_id, "case_id": req.case_id, "reply": reply}

    @app.post("/consolidate")
    async def consolidate_route(req: ConsolidateRequest) -> dict[str, object]:
        try:
            result = await consolidate(req.case_id, req.task)
        except Exception as exc:
            raise HTTPException(500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {
            "case_id": req.case_id,
            "task": req.task,
            "patterns_promoted": result.patterns_promoted,
            "patterns_rejected": result.patterns_rejected,
            "lesson_ids": list(result.lesson_ids),
        }

    @app.post("/optimize/skill")
    async def optimize_skill_route(req: OptimizeSkillRequest) -> dict[str, object]:
        try:
            outcomes = await optimize_skill(req.case_id, req.task, req.skill)
        except Exception as exc:
            raise HTTPException(500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {
            "case_id": req.case_id,
            "skill": req.skill,
            "task": req.task,
            "outcomes": [o.model_dump(mode="json") for o in outcomes],
        }

    @app.get("/teams")
    async def teams_info() -> dict[str, object]:
        return {
            "teams": {
                INTAKE_TEAM: {
                    "leader": agent_engine.team_leader(INTAKE_TEAM),
                    "members": agent_engine.team_members(INTAKE_TEAM),
                },
                LITIGATION_TEAM: {
                    "leader": agent_engine.team_leader(LITIGATION_TEAM),
                    "members": agent_engine.team_members(LITIGATION_TEAM),
                },
            }
        }

    @app.post("/intake/turn")
    async def intake_turn_route(req: TeamTurnRequest) -> dict[str, object]:
        try:
            reply = await intake_turn(req.session_id, req.case_id, req.message)
        except Exception as exc:
            raise HTTPException(500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {"session_id": req.session_id, "case_id": req.case_id, "reply": reply}

    @app.post("/litigation/turn")
    async def litigation_turn_route(req: TeamTurnRequest) -> dict[str, object]:
        try:
            reply = await litigation_turn(req.session_id, req.case_id, req.message)
        except Exception as exc:
            raise HTTPException(500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {"session_id": req.session_id, "case_id": req.case_id, "reply": reply}

    @app.post("/workflow/run")
    async def workflow_run_route(req: WorkflowRunRequest) -> dict[str, object]:
        try:
            output = await run_workflow(
                req.session_id, req.case_id, req.client_name, req.matter_summary
            )
        except Exception as exc:
            raise HTTPException(500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {"session_id": req.session_id, "case_id": req.case_id, "output": output}

    @app.post("/workflow/resume")
    async def workflow_resume_route(req: WorkflowResumeRequest) -> dict[str, object]:
        try:
            output = await resume_workflow(req.session_id, req.case_id)
        except Exception as exc:
            raise HTTPException(500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {"session_id": req.session_id, "case_id": req.case_id, "output": output}
