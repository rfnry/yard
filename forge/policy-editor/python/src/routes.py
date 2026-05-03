from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from rfnry import build_scope

from src.agent import run_turn

SEEDS_DIR: Path = Path(__file__).resolve().parent.parent.parent / "seeds"
DATA_DIR: Path = Path(__file__).resolve().parent.parent.parent / "data"


class InitRequest(BaseModel):
    policy_id: str


class TurnRequest(BaseModel):
    session_id: str
    policy_id: str
    message: str


class ListRequest(BaseModel):
    policy_id: str


def _scope_dir(policy_id: str) -> Path:
    leaf = build_scope(["policy_id"], {"policy_id": policy_id}).leaf
    return DATA_DIR / leaf


def register(app: FastAPI) -> None:
    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/init")
    async def init(req: InitRequest) -> dict[str, object]:
        target = _scope_dir(req.policy_id)
        target.mkdir(parents=True, exist_ok=True)
        copied: list[str] = []
        for src in sorted(SEEDS_DIR.iterdir()):
            if src.is_file():
                shutil.copy2(src, target / src.name)
                copied.append(src.name)
        return {"policy_id": req.policy_id, "data_dir": str(target), "files": copied}

    @app.post("/turn")
    async def turn(req: TurnRequest, request: Request) -> dict[str, object]:
        target = _scope_dir(req.policy_id)
        if not target.exists():
            raise HTTPException(
                status_code=404,
                detail=f"policy_id {req.policy_id!r} not initialized; POST /init first",
            )
        try:
            reply = await run_turn(
                request.app.state.agent,
                session_id=req.session_id,
                message=req.message,
                scope={"policy_id": req.policy_id},
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc
        return {"session_id": req.session_id, "policy_id": req.policy_id, "reply": reply}

    @app.post("/list")
    async def list_files(req: ListRequest) -> dict[str, object]:
        target = _scope_dir(req.policy_id)
        if not target.exists():
            raise HTTPException(status_code=404, detail=f"policy_id {req.policy_id!r} not initialized")
        files: list[dict[str, object]] = []
        for f in sorted(target.iterdir()):
            if f.is_file():
                files.append(
                    {
                        "name": f.name,
                        "size": f.stat().st_size,
                        "preview": f.read_text(encoding="utf-8")[:200],
                    }
                )
        return {"policy_id": req.policy_id, "files": files}
