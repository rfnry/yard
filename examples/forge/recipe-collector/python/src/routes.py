from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from rfnry_forge.parser import default_registry
from rfnry_rag import RagEngine
from rfnry_rag.exceptions import DuplicateSourceError, IngestionError, SourceNotFoundError

from src.rag import DEFAULT_KNOWLEDGE_ID
from src.schemas import (
    CountDelta,
    FidelityReport,
    IngestResponse,
    QueryRequest,
    QueryResponse,
    SourceCitation,
    VerifyRequest,
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
        knowledge_id: str | None = Form(None),
    ) -> IngestResponse:
        rag = _engine(request)
        suffix = Path(file.filename or "upload").suffix or ".pdf"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = Path(tmp.name)
        try:
            try:
                source = await rag.ingest(
                    file_path=str(tmp_path),
                    knowledge_id=knowledge_id or DEFAULT_KNOWLEDGE_ID,
                    source_type="recipe",
                    metadata={"original_filename": file.filename or ""},
                )
            except DuplicateSourceError as exc:
                raise HTTPException(status_code=409, detail=str(exc)) from exc
            except IngestionError as exc:
                raise HTTPException(status_code=422, detail=str(exc)) from exc
        finally:
            tmp_path.unlink(missing_ok=True)
        return IngestResponse(source_id=source.source_id, chunk_count=source.chunk_count)

    @app.post("/query", response_model=QueryResponse)
    async def query(req: QueryRequest, request: Request) -> QueryResponse:
        rag = _engine(request)
        result = await rag.query(
            text=req.query,
            knowledge_id=req.knowledge_id or DEFAULT_KNOWLEDGE_ID,
        )
        return QueryResponse(
            answer=result.answer or "",
            sources=[
                SourceCitation(source_id=s.source_id, page_number=s.page_number, score=s.score)
                for s in result.sources
            ],
        )

    @app.post("/verify-source", response_model=FidelityReport)
    async def verify_source(req: VerifyRequest, request: Request) -> FidelityReport:
        rag = _engine(request)
        raw_path = Path(req.raw_path)
        if not raw_path.is_absolute():
            raw_path = (Path(__file__).resolve().parent.parent.parent / raw_path).resolve()
        if not raw_path.exists():
            raise HTTPException(status_code=404, detail=f"raw_path not found: {raw_path}")

        try:
            chunks = await rag.knowledge.get_chunks(source_id=req.source_id)
        except SourceNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        stored_text = "\n".join(c.content for c in chunks)
        raw_text = raw_path.read_text(encoding="utf-8")

        parser = default_registry.detect_for(str(raw_path), raw_text)
        before = parser.parse(raw_text)
        after = parser.parse(stored_text)
        delta = parser.diff(before, after)
        sim = parser.similarity(before, after)

        notes = _summarize(parser.domain, delta, sim)

        return FidelityReport(
            source_id=req.source_id,
            raw_path=str(raw_path),
            parser_used=parser.domain,
            similarity=sim,
            deletion_paths=delta.deletion_paths,
            corruption_paths=[c.model_dump(mode="json") for c in delta.corruption_paths],
            count_delta=CountDelta(
                counts_before=delta.counts_before,
                counts_after=delta.counts_after,
            ),
            notes=notes,
        )


def _summarize(domain: str, delta, similarity: float) -> str:
    if delta.is_clean and similarity >= 0.99:
        return f"{domain}: chunked content matches source ({similarity:.2f})."
    parts: list[str] = [f"parser={domain}", f"similarity={similarity:.2f}"]
    if delta.deletion_paths:
        parts.append(f"missing={delta.deletion_paths}")
    if delta.corruption_paths:
        parts.append(f"changed={[c.path for c in delta.corruption_paths]}")
    return "; ".join(parts)
