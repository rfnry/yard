from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel


class TurnRequest(BaseModel):
    session_id: str
    org_id: str
    user_id: str
    message: str
    task: str | None = "support"


class ResumeRequest(BaseModel):
    session_id: str
    org_id: str
    user_id: str
    task: str | None = "support"


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
                scope={"org_id": req.org_id, "user_id": req.user_id},
                task=req.task,
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {
            "session_id": req.session_id,
            "scope_leaf": f"{req.org_id}/{req.user_id}",
            "reply": reply,
        }

    @app.post("/resume")
    async def resume(req: ResumeRequest, request: Request) -> dict[str, str]:
        agent = request.app.state.agent
        reply = await agent.resume(
            session_id=req.session_id,
            scope={"org_id": req.org_id, "user_id": req.user_id},
            task=req.task,
        )
        return {"session_id": req.session_id, "reply": reply}
