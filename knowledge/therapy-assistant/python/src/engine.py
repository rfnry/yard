from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from rfnry_knowledge import (
    DefaultMemoryExtractor,
    MemoryEngine,
    MemoryEngineConfig,
    MemoryIngestionConfig,
    MemoryRetrievalConfig,
    QdrantVectorStore,
)

from src.providers import Settings, embeddings, extractor_provider


def build_config(settings: Settings) -> MemoryEngineConfig:
    embedder = embeddings(settings)
    extractor = DefaultMemoryExtractor(provider_client=extractor_provider(settings))

    vector_store = QdrantVectorStore(
        url=settings.qdrant_url,
        collection=settings.qdrant_collection,
    )

    return MemoryEngineConfig(
        ingestion=MemoryIngestionConfig(
            extractor=extractor,
            embeddings=embedder,
            vector_store=vector_store,
            dedup_context_top_k=5,
        ),
        retrieval=MemoryRetrievalConfig(
            semantic_weight=1.0,
            keyword_weight=0.0,
            entity_weight=0.0,
        ),
    )


@asynccontextmanager
async def lifespan_engine() -> AsyncIterator[MemoryEngine]:
    settings = Settings.from_env()
    engine = MemoryEngine(build_config(settings))
    async with engine:
        yield engine
