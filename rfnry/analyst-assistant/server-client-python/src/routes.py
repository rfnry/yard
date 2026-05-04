from __future__ import annotations

import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.engine import agent_engine, consolidate, resume, turn


class TurnRequest(BaseModel):
    session_id: str
    client_id: str
    message: str
    task: str | None = None


class ResumeRequest(BaseModel):
    session_id: str
    client_id: str


class ConsolidateRequest(BaseModel):
    client_id: str
    task: str


def register(app: FastAPI) -> None:
    @app.post("/turn")
    async def turn_route(req: TurnRequest) -> dict[str, object]:
        try:
            reply = await turn(req.session_id, req.client_id, req.message, req.task)
        except Exception as exc:
            raise HTTPException(500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {"session_id": req.session_id, "client_id": req.client_id, "reply": reply}

    @app.post("/resume")
    async def resume_route(req: ResumeRequest) -> dict[str, object]:
        reply = await resume(req.session_id, req.client_id)
        return {"session_id": req.session_id, "client_id": req.client_id, "reply": reply}

    @app.post("/consolidate")
    async def consolidate_route(req: ConsolidateRequest) -> dict[str, object]:
        try:
            result = await consolidate(req.client_id, req.task)
        except Exception as exc:
            raise HTTPException(500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {
            "client_id": req.client_id,
            "task": req.task,
            "patterns_promoted": result.patterns_promoted,
            "patterns_rejected": result.patterns_rejected,
            "lesson_ids": list(result.lesson_ids),
        }

    @app.get("/telemetry/{client_id}")
    async def telemetry_route(client_id: str) -> dict[str, object]:
        runner = agent_engine.runner()
        db_path = Path(runner.root) / "data" / client_id / "state.db"
        if not db_path.exists():
            return {"client_id": client_id, "rows": [], "totals": {}}
        conn = sqlite3.connect(db_path)
        try:
            conn.row_factory = sqlite3.Row
            rows = list(conn.execute("SELECT * FROM telemetry ORDER BY at DESC LIMIT 200"))
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
