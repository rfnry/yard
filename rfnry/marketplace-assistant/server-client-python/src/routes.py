from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.engine import resume, turn


class TurnRequest(BaseModel):
    session_id: str
    message: str


class ResumeRequest(BaseModel):
    session_id: str


def register(app: FastAPI) -> None:
    @app.post("/turn")
    async def turn_route(req: TurnRequest) -> dict[str, str]:
        try:
            reply = await turn(req.session_id, req.message)
        except Exception as exc:
            raise HTTPException(500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {"session_id": req.session_id, "reply": reply}

    @app.post("/resume")
    async def resume_route(req: ResumeRequest) -> dict[str, str]:
        reply = await resume(req.session_id)
        return {"session_id": req.session_id, "reply": reply}
