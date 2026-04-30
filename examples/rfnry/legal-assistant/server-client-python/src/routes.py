from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel


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


def register(app: FastAPI) -> None:
    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/turn")
    async def turn(req: TurnRequest, request: Request) -> dict[str, object]:
        agent = request.app.state.agent
        try:
            reply = await agent.turn(
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
        agent = request.app.state.agent
        reply = await agent.resume(
            session_id=req.session_id,
            scope={"case_id": req.case_id},
            task=req.task,
        )
        return {"session_id": req.session_id, "case_id": req.case_id, "reply": reply}

    @app.post("/consolidate")
    async def consolidate(req: ConsolidateRequest, request: Request) -> dict[str, object]:
        agent = request.app.state.agent
        try:
            result = await agent.consolidate(task=req.task, scope={"case_id": req.case_id})
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {
            "case_id": req.case_id,
            "task": req.task,
            "patterns_promoted": result.patterns_promoted,
            "patterns_rejected": result.patterns_rejected,
            "lessons_refs": [str(p) for p in result.lessons_refs],
        }
