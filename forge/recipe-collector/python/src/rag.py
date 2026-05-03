from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from rfnry_rag import (
    DocumentIngestion,
    DocumentRetrieval,
    Embeddings,
    GenerationConfig,
    IngestionConfig,
    LanguageModel,
    LanguageModelClient,
    PostgresDocumentStore,
    QdrantVectorStore,
    QueryMode,
    RagEngine,
    RagEngineConfig,
    RetrievalConfig,
    RoutingConfig,
    SQLAlchemyMetadataStore,
    VectorIngestion,
    VectorRetrieval,
)

DEFAULT_KNOWLEDGE_ID = os.environ.get("KNOWLEDGE_ID", "recipes")

_RECIPE_SYSTEM_PROMPT = (
    "You answer cooking questions using only the provided recipe context. "
    "Cite source ids and quote exact quantities and ingredient names from "
    "the context — do not paraphrase or convert units. If the context does "
    "not contain the answer, say so plainly."
)


def _require(env: str) -> str:
    value = os.environ.get(env, "").strip()
    if not value:
        raise RuntimeError(f"{env} must be set")
    return value


def _generation_client() -> LanguageModelClient:
    return LanguageModelClient(
        lm=LanguageModel(
            provider="anthropic",
            model=os.environ.get("GENERATION_MODEL", "claude-sonnet-4-6"),
            api_key=_require("ANTHROPIC_API_KEY"),
        ),
    )


def _build_config() -> RagEngineConfig:
    openai_key = _require("OPENAI_API_KEY")

    embeddings = Embeddings(
        LanguageModel(
            provider="openai",
            model=os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small"),
            api_key=openai_key,
        )
    )
    vector_store = QdrantVectorStore(
        url=os.environ.get("QDRANT_URL", "http://localhost:6333"),
        collection=os.environ.get("QDRANT_COLLECTION", "recipe-collector"),
    )
    metadata_store = SQLAlchemyMetadataStore(url=_require("POSTGRES_URL"))
    document_store = PostgresDocumentStore(url=_require("POSTGRES_URL"))
    embedding_model_name = f"openai:{embeddings.model}"

    ingestion = IngestionConfig(
        methods=[
            VectorIngestion(
                store=vector_store,
                embeddings=embeddings,
                embedding_model_name=embedding_model_name,
            ),
            DocumentIngestion(store=document_store),
        ],
        chunk_size=300,
        chunk_overlap=40,
    )
    retrieval = RetrievalConfig(
        methods=[
            VectorRetrieval(
                store=vector_store,
                embeddings=embeddings,
                bm25_enabled=True,
                weight=1.0,
            ),
            DocumentRetrieval(store=document_store, weight=0.6),
        ],
        top_k=6,
    )
    generation = GenerationConfig(
        lm_client=_generation_client(),
        system_prompt=_RECIPE_SYSTEM_PROMPT,
        grounding_enabled=True,
        grounding_threshold=0.4,
    )
    routing = RoutingConfig(mode=QueryMode.AUTO, full_context_threshold=80_000)

    return RagEngineConfig(
        metadata_store=metadata_store,
        ingestion=ingestion,
        retrieval=retrieval,
        generation=generation,
        routing=routing,
    )


@asynccontextmanager
async def lifespan_engine() -> AsyncIterator[RagEngine]:
    engine = RagEngine(_build_config())
    async with engine:
        yield engine
