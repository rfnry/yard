from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from src.agent import run_consolidate, run_optimize_skill, run_resume, run_turn


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


def register(app: FastAPI) -> None:
    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/turn")
    async def turn(req: TurnRequest, request: Request) -> dict[str, object]:
        try:
            reply = await run_turn(
                request.app.state.agent,
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
            request.app.state.agent,
            session_id=req.session_id,
            scope={"case_id": req.case_id},
            task=req.task,
        )
        return {"session_id": req.session_id, "case_id": req.case_id, "reply": reply}

    @app.post("/consolidate")
    async def consolidate(req: ConsolidateRequest, request: Request) -> dict[str, object]:
        try:
            result = await run_consolidate(
                request.app.state.agent,
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
    async def optimize_skill(
        req: OptimizeSkillRequest, request: Request
    ) -> dict[str, object]:
        try:
            outcomes = await run_optimize_skill(
                request.app.state.agent,
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
