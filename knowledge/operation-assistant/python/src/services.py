"""Business operations for the operation-assistant.

Routes parse HTTP, services do work. Each function takes the engine + DTOs and
returns DTOs — no FastAPI types here.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import UploadFile
from rfnry_knowledge import KnowledgeEngine

from src.providers import Settings
from src.schemas import (
    IngestResponse,
    KnowledgeListResponse,
    QueryResponse,
    SourceCitation,
    SourceInfo,
    SourceType,
)


async def ingest_upload(
    *,
    engine: KnowledgeEngine,
    file: UploadFile,
    source_type: SourceType,
    knowledge_id: str | None,
    tags: str | None,
    settings: Settings,
) -> IngestResponse:
    """Persist the uploaded file to a temp path and run it through the engine."""
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
        source = await engine.ingest(
            file_path=str(tmp_path),
            knowledge_id=knowledge_id or settings.knowledge_id,
            source_type=source_type,
            metadata=metadata,
        )
    finally:
        tmp_path.unlink(missing_ok=True)

    return IngestResponse(
        source_id=source.source_id,
        source_type=source_type,
        chunk_count=source.chunk_count,
    )


async def answer_query(
    *,
    engine: KnowledgeEngine,
    query: str,
    knowledge_id: str | None,
    settings: Settings,
) -> QueryResponse:
    result = await engine.query(
        text=query,
        knowledge_id=knowledge_id or settings.knowledge_id,
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


async def list_knowledge(
    *,
    engine: KnowledgeEngine,
    knowledge_id: str | None,
    settings: Settings,
) -> KnowledgeListResponse:
    kid = knowledge_id or settings.knowledge_id
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


async def remove_source(
    *,
    engine: KnowledgeEngine,
    source_id: str,
) -> int:
    return await engine.knowledge.remove(source_id=source_id)
