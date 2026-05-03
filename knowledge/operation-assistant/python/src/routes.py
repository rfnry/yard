"""HTTP plumbing — parse request, call service, map errors. No business logic."""

from __future__ import annotations

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from rfnry_knowledge import KnowledgeEngine
from rfnry_knowledge.exceptions import DuplicateSourceError, IngestionError

from src import services
from src.providers import Settings
from src.schemas import (
    IngestResponse,
    KnowledgeListResponse,
    QueryRequest,
    QueryResponse,
    SourceType,
)


def _engine(request: Request) -> KnowledgeEngine:
    return request.app.state.engine


def _settings(request: Request) -> Settings:
    return request.app.state.settings


def register(app: FastAPI) -> None:
    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/ingest", response_model=IngestResponse)
    async def ingest(
        request: Request,
        file: UploadFile = File(...),
        source_type: SourceType = Form(...),
        knowledge_id: str | None = Form(None),
        tags: str | None = Form(None),
    ) -> IngestResponse:
        try:
            return await services.ingest_upload(
                engine=_engine(request),
                file=file,
                source_type=source_type,
                knowledge_id=knowledge_id,
                tags=tags,
                settings=_settings(request),
            )
        except DuplicateSourceError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        except IngestionError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/query", response_model=QueryResponse)
    async def query(req: QueryRequest, request: Request) -> QueryResponse:
        return await services.answer_query(
            engine=_engine(request),
            query=req.query,
            knowledge_id=req.knowledge_id,
            settings=_settings(request),
        )

    @app.get("/knowledge", response_model=KnowledgeListResponse)
    async def knowledge(request: Request, knowledge_id: str | None = None) -> KnowledgeListResponse:
        return await services.list_knowledge(
            engine=_engine(request),
            knowledge_id=knowledge_id,
            settings=_settings(request),
        )

    @app.delete("/sources/{source_id}")
    async def delete_source(source_id: str, request: Request) -> dict[str, int | str]:
        removed = await services.remove_source(engine=_engine(request), source_id=source_id)
        if removed == 0:
            raise HTTPException(status_code=404, detail=f"source {source_id!r} not found")
        return {"source_id": source_id, "removed": removed}
