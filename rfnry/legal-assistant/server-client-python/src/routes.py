from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from src.agent import run_consolidate, run_optimize_skill, run_resume, run_turn
from src.agent.server import LEADER_NAME, TEAM_NAME, WORKFLOW_NAME


class TurnRequest(BaseModel):
    session_id: str
    case_id: str
    message: str
    task: str | None = "investigate"


class ResumeRequest(BaseModel):
    session_id: str
    case_id: str
    task: str | None = "investigate"


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
    request: str


class WorkflowResumeRequest(BaseModel):
    session_id: str
    case_id: str


def register(app: FastAPI) -> None:
    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    # ---------------------------------------------------------------- single agent
    # The records-investigator alone, dispatched by (team, agent). Same surface
    # as before the engine refactor — useful for direct tool exercises and the
    # /consolidate and /optimize/skill paths that target one member's task.

    @app.post("/turn")
    async def turn(req: TurnRequest, request: Request) -> dict[str, object]:
        try:
            reply = await run_turn(
                request.app.state.engine,
                session_id=req.session_id,
                message=req.message,
                scope={"case_id": req.case_id},
                task=req.task,
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {"session_id": req.session_id, "case_id": req.case_id, "reply": reply}

    @app.post("/resume")
    async def resume(req: ResumeRequest, request: Request) -> dict[str, object]:
        reply = await run_resume(
            request.app.state.engine,
            session_id=req.session_id,
            scope={"case_id": req.case_id},
            task=req.task,
        )
        return {"session_id": req.session_id, "case_id": req.case_id, "reply": reply}

    @app.post("/consolidate")
    async def consolidate(req: ConsolidateRequest, request: Request) -> dict[str, object]:
        try:
            result = await run_consolidate(
                request.app.state.engine,
                scope={"case_id": req.case_id},
                task=req.task,
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {
            "case_id": req.case_id,
            "task": req.task,
            "patterns_promoted": result.patterns_promoted,
            "patterns_rejected": result.patterns_rejected,
            "lesson_ids": list(result.lesson_ids),
        }

    @app.post("/optimize/skill")
    async def optimize_skill(req: OptimizeSkillRequest, request: Request) -> dict[str, object]:
        try:
            outcomes = await run_optimize_skill(
                request.app.state.engine,
                scope={"case_id": req.case_id},
                task=req.task,
                skill=req.skill,
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {
            "case_id": req.case_id,
            "skill": req.skill,
            "task": req.task,
            "outcomes": [o.model_dump(mode="json") for o in outcomes],
        }

    # -------------------------------------------------------------------------- team
    # The case-strategist (leader) decides delegation dynamically.

    @app.get("/team")
    async def team_info(request: Request) -> dict[str, object]:
        engine = request.app.state.engine
        return {
            "name": TEAM_NAME,
            "leader": engine.team_leader(TEAM_NAME),
            "members": engine.team_members(TEAM_NAME),
        }

    @app.post("/team/turn")
    async def team_turn(req: TeamTurnRequest, request: Request) -> dict[str, object]:
        try:
            reply = await request.app.state.engine.turn(
                session_id=req.session_id,
                message=req.message,
                scope={"case_id": req.case_id},
                team=TEAM_NAME,
                agent=LEADER_NAME,
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {"session_id": req.session_id, "case_id": req.case_id, "reply": reply}

    # ---------------------------------------------------------------------- workflow
    # The same three agents in a deterministic, observable, resumable pipeline.

    @app.post("/workflow/run")
    async def workflow_run(req: WorkflowRunRequest, request: Request) -> dict[str, object]:
        try:
            output = await request.app.state.engine.run_workflow(
                name=WORKFLOW_NAME,
                session_id=req.session_id,
                input={"case_id": req.case_id, "request": req.request},
                scope={"case_id": req.case_id},
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {"session_id": req.session_id, "case_id": req.case_id, "output": output}

    @app.post("/workflow/resume")
    async def workflow_resume(req: WorkflowResumeRequest, request: Request) -> dict[str, object]:
        try:
            output = await request.app.state.engine.resume_workflow(
                name=WORKFLOW_NAME,
                session_id=req.session_id,
                scope={"case_id": req.case_id},
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {"session_id": req.session_id, "case_id": req.case_id, "output": output}
