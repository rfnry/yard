from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from rfnry import AgentEngine
from rfnry_knowledge import KnowledgeEngine
from rfnry_knowledge.exceptions import DuplicateSourceError, IngestionError

from src.agent import run_resume, run_turn
from src.schemas import (
    IngestResponse,
    KnowledgeListResponse,
    MessageRequest,
    MessageResponse,
    SourceInfo,
    SourceType,
)
from src.settings import Settings

_INGEST_TYPE_MAP: dict[SourceType, str] = {
    "manual": "manual",
    "drawing": "drawing",
    "transcript": "manual",
}


def _agent(request: Request) -> AgentEngine:
    return request.app.state.agent


def _knowledge(request: Request) -> KnowledgeEngine:
    return request.app.state.knowledge


def _settings(request: Request) -> Settings:
    return request.app.state.settings


def register(app: FastAPI) -> None:
    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/threads/{thread_id}/messages", response_model=MessageResponse)
    async def post_message(
        thread_id: str, req: MessageRequest, request: Request
    ) -> MessageResponse:
        try:
            reply = await run_turn(
                _agent(request),
                session_id=thread_id,
                message=req.message,
                scope={},
                task="assist-technician",
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc
        return MessageResponse(thread_id=thread_id, reply=reply)

    @app.post("/threads/{thread_id}/resume", response_model=MessageResponse)
    async def resume_thread(thread_id: str, request: Request) -> MessageResponse:
        reply = await run_resume(
            _agent(request),
            session_id=thread_id,
            scope={},
            task="assist-technician",
        )
        return MessageResponse(thread_id=thread_id, reply=reply)

    @app.post("/ingest", response_model=IngestResponse)
    async def ingest(
        request: Request,
        file: UploadFile = File(...),
        source_type: SourceType = Form(...),
        knowledge_id: str | None = Form(None),
        tags: str | None = Form(None),
    ) -> IngestResponse:
        suffix = Path(file.filename or "upload").suffix or ".pdf"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = Path(tmp.name)

        engine_source_type = _INGEST_TYPE_MAP[source_type]
        tag_list = [t.strip() for t in (tags or "").split(",") if t.strip()]
        if source_type == "transcript" and "transcript" not in tag_list:
            tag_list.append("transcript")

        try:
            try:
                source = await _knowledge(request).ingest(
                    file_path=str(tmp_path),
                    knowledge_id=knowledge_id or _settings(request).knowledge_id,
                    source_type=engine_source_type,
                    metadata={
                        "original_filename": file.filename or "",
                        "tags": tag_list,
                    },
                )
            except DuplicateSourceError as exc:
                raise HTTPException(status_code=409, detail=str(exc)) from exc
            except IngestionError as exc:
                raise HTTPException(status_code=422, detail=str(exc)) from exc
        finally:
            tmp_path.unlink(missing_ok=True)

        return IngestResponse(
            source_id=source.source_id,
            source_type=source_type,
            chunk_count=source.chunk_count,
        )

    @app.get("/knowledge", response_model=KnowledgeListResponse)
    async def knowledge(request: Request, knowledge_id: str | None = None) -> KnowledgeListResponse:
        kid = knowledge_id or _settings(request).knowledge_id
        engine = _knowledge(request)
        sources = await engine.knowledge.list(knowledge_id=kid)
        corpus_tokens = await engine.knowledge.get_corpus_tokens(knowledge_id=kid)
        return KnowledgeListResponse(
            knowledge_id=kid,
            sources=[
                SourceInfo(
                    source_id=s.source_id,
                    source_type=s.source_type,
                    chunk_count=s.chunk_count,
                    tags=s.tags,
                )
                for s in sources
            ],
            total_chunks=sum(s.chunk_count for s in sources),
            estimated_tokens=corpus_tokens,
        )

    @app.delete("/sources/{source_id}")
    async def delete_source(source_id: str, request: Request) -> dict[str, int | str]:
        removed = await _knowledge(request).knowledge.remove(source_id=source_id)
        if removed == 0:
            raise HTTPException(status_code=404, detail=f"source {source_id!r} not found")
        return {"source_id": source_id, "removed": removed}
