from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from rfnry_rag import RagEngine
from rfnry_rag.exceptions import DuplicateSourceError, IngestionError

from src.rag import DEFAULT_KNOWLEDGE_ID
from src.schemas import (
    IngestResponse,
    KnowledgeListResponse,
    QueryRequest,
    QueryResponse,
    SourceCitation,
    SourceInfo,
    SourceType,
)


def _engine(request: Request) -> RagEngine:
    return request.app.state.rag


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
        rag = _engine(request)
        suffix = Path(file.filename or "upload").suffix or ".pdf"

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = Path(tmp.name)

        try:
            tag_list = [t.strip() for t in (tags or "").split(",") if t.strip()]
            metadata = {
                "original_filename": file.filename or "",
                "tags": tag_list,
            }
            try:
                source = await rag.ingest(
                    file_path=str(tmp_path),
                    knowledge_id=knowledge_id or DEFAULT_KNOWLEDGE_ID,
                    source_type=source_type,
                    metadata=metadata,
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

    @app.post("/query", response_model=QueryResponse)
    async def query(req: QueryRequest, request: Request) -> QueryResponse:
        rag = _engine(request)
        knowledge_id = req.knowledge_id or DEFAULT_KNOWLEDGE_ID
        result = await rag.query(
            text=req.query,
            knowledge_id=knowledge_id,
            trace=True,
        )
        trace = result.trace
        return QueryResponse(
            answer=result.answer or "",
            routing=trace.routing_decision if trace else None,
            grounding=trace.grounding_decision if trace else None,
            sources=[
                SourceCitation(
                    source_id=s.source_id,
                    page_number=s.page_number,
                    score=s.score,
                )
                for s in result.sources
            ],
        )

    @app.get("/knowledge", response_model=KnowledgeListResponse)
    async def knowledge(request: Request, knowledge_id: str | None = None) -> KnowledgeListResponse:
        rag = _engine(request)
        kid = knowledge_id or DEFAULT_KNOWLEDGE_ID
        sources = await rag.knowledge.list(knowledge_id=kid)
        corpus_tokens = await rag.knowledge.get_corpus_tokens(knowledge_id=kid)
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
        rag = _engine(request)
        removed = await rag.knowledge.remove(source_id=source_id)
        if removed == 0:
            raise HTTPException(status_code=404, detail=f"source {source_id!r} not found")
        return {"source_id": source_id, "removed": removed}
