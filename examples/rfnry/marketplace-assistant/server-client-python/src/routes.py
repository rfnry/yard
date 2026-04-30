from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel


class TurnRequest(BaseModel):
    session_id: str
    message: str
    task: str | None = "team-lookup"


class ResumeRequest(BaseModel):
    session_id: str
    task: str | None = "team-lookup"


def register(app: FastAPI) -> None:
    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/turn")
    async def turn(req: TurnRequest, request: Request) -> dict[str, str]:
        agent = request.app.state.agent
        try:
            reply = await agent.turn(
                session_id=req.session_id,
                message=req.message,
                scope={},
                task=req.task,
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {"session_id": req.session_id, "reply": reply}

    @app.post("/resume")
    async def resume(req: ResumeRequest, request: Request) -> dict[str, str]:
        agent = request.app.state.agent
        reply = await agent.resume(session_id=req.session_id, scope={}, task=req.task)
        return {"session_id": req.session_id, "reply": reply}
