from __future__ import annotations

import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from src.agent import run_consolidate, run_resume, run_turn


class TurnRequest(BaseModel):
    session_id: str
    client_id: str
    message: str
    task: str | None = None


class ResumeRequest(BaseModel):
    session_id: str
    client_id: str
    task: str | None = None


class ConsolidateRequest(BaseModel):
    client_id: str
    task: str


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
                scope={"client_id": req.client_id},
                task=req.task,
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {"session_id": req.session_id, "client_id": req.client_id, "reply": reply}

    @app.post("/resume")
    async def resume(req: ResumeRequest, request: Request) -> dict[str, object]:
        reply = await run_resume(
            request.app.state.agent,
            session_id=req.session_id,
            scope={"client_id": req.client_id},
            task=req.task,
        )
        return {"session_id": req.session_id, "client_id": req.client_id, "reply": reply}

    @app.post("/consolidate")
    async def consolidate(req: ConsolidateRequest, request: Request) -> dict[str, object]:
        try:
            result = await run_consolidate(
                request.app.state.agent,
                scope={"client_id": req.client_id},
                task=req.task,
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {
            "client_id": req.client_id,
            "task": req.task,
            "patterns_promoted": result.patterns_promoted,
            "patterns_rejected": result.patterns_rejected,
            "lesson_ids": list(result.lesson_ids),
        }

    @app.get("/telemetry/{client_id}")
    async def telemetry(client_id: str, request: Request) -> dict[str, object]:
        agent = request.app.state.agent
        db_path = Path(agent.root) / "data" / client_id / "state.db"
        if not db_path.exists():
            return {"client_id": client_id, "rows": [], "totals": {}}
        conn = sqlite3.connect(db_path)
        try:
            conn.row_factory = sqlite3.Row
            rows = list(
                conn.execute(
                    "SELECT * FROM telemetry ORDER BY at DESC LIMIT 200",
                )
            )
            totals_row = conn.execute(
                """
                SELECT
                    COUNT(*) AS turns,
                    COALESCE(SUM(tokens_input), 0) AS input,
                    COALESCE(SUM(tokens_output), 0) AS output,
                    COALESCE(SUM(tokens_cache_creation), 0) AS cache_creation,
                    COALESCE(SUM(tokens_cache_read), 0) AS cache_read,
                    COALESCE(SUM(duration_ms), 0) AS duration_ms,
                    COALESCE(SUM(tool_calls), 0) AS tool_calls,
                    COALESCE(SUM(tool_errors), 0) AS tool_errors
                FROM telemetry
                """
            ).fetchone()
        finally:
            conn.close()
        return {
            "client_id": client_id,
            "rows": [dict(r) for r in rows],
            "totals": dict(totals_row) if totals_row is not None else {},
        }
