from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from rfnry_rag import (
    DocumentIngestion,
    DocumentRetrieval,
    Embeddings,
    GenerationConfig,
    GraphIngestion,
    GraphRetrieval,
    IngestionConfig,
    LanguageModelClient,
    LanguageModelProvider,
    Neo4jGraphStore,
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
    Vision,
)
from rfnry_rag.config import DrawingIngestionConfig, GraphIngestionConfig

DEFAULT_KNOWLEDGE_ID = os.environ.get("KNOWLEDGE_ID", "machines")
_FULL_CONTEXT_THRESHOLD = int(os.environ.get("FULL_CONTEXT_THRESHOLD", "150000"))

_OPERATION_SYSTEM_PROMPT = (
    "You are a factory operations assistant. Use only the provided context — extracted "
    "from machine manuals and mechanical drawings — to answer technician questions. "
    "Cite source ids and page numbers. Reference specific components, wiring connections, "
    "and procedure steps. If the context does not contain the answer, say so plainly."
)


def _require(env: str) -> str:
    value = os.environ.get(env, "").strip()
    if not value:
        raise RuntimeError(f"{env} must be set")
    return value


def _generation_client() -> LanguageModelClient:
    return LanguageModelClient(
        provider=LanguageModelProvider(
            provider="anthropic",
            model=os.environ.get("GENERATION_MODEL", "claude-sonnet-4-5"),
            api_key=_require("ANTHROPIC_API_KEY"),
        ),
    )


def _build_config() -> RagEngineConfig:
    openai_key = _require("OPENAI_API_KEY")
    anthropic_key = _require("ANTHROPIC_API_KEY")

    embeddings = Embeddings(
        LanguageModelProvider(
            provider="openai",
            model=os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small"),
            api_key=openai_key,
        )
    )
    vision = Vision(
        LanguageModelProvider(
            provider="anthropic",
            model=os.environ.get("VISION_MODEL", "claude-sonnet-4-5"),
            api_key=anthropic_key,
        )
    )

    vector_store = QdrantVectorStore(
        url=os.environ.get("QDRANT_URL", "http://localhost:6333"),
        collection=os.environ.get("QDRANT_COLLECTION", "operation-assistant"),
    )
    metadata_store = SQLAlchemyMetadataStore(url=_require("POSTGRES_URL"))
    document_store = PostgresDocumentStore(url=_require("POSTGRES_URL"))
    graph_store = Neo4jGraphStore(
        uri=os.environ.get("NEO4J_URL", "bolt://localhost:7687"),
        username=os.environ.get("NEO4J_USER", "neo4j"),
        password=_require("NEO4J_PASSWORD"),
    )

    embedding_model_name = f"openai:{embeddings.model}"
    graph_ingestion_lm = _generation_client()

    ingestion = IngestionConfig(
        methods=[
            VectorIngestion(
                store=vector_store,
                embeddings=embeddings,
                embedding_model_name=embedding_model_name,
            ),
            DocumentIngestion(store=document_store),
            GraphIngestion(
                store=graph_store,
                lm_client=graph_ingestion_lm,
                graph_config=GraphIngestionConfig(
                    relationship_keyword_map={
                        "connected": "CONNECTS_TO",
                        "wired": "CONNECTS_TO",
                        "feeds": "FEEDS",
                        "controls": "CONTROLLED_BY",
                        "mounted": "REFERENCES",
                    },
                    unclassified_relation_default="MENTIONS",
                ),
            ),
        ],
        embeddings=embeddings,
        vision=vision,
        lm_client=graph_ingestion_lm,
        chunk_size=375,
        chunk_overlap=40,
        analyze_concurrency=5,
        drawings=DrawingIngestionConfig(
            enabled=True,
            lm_client=_generation_client(),
            dpi=400,
            analyze_concurrency=3,
        ),
    )

    retrieval = RetrievalConfig(
        methods=[
            VectorRetrieval(
                store=vector_store,
                embeddings=embeddings,
                bm25_enabled=True,
                weight=1.0,
            ),
            DocumentRetrieval(store=document_store, weight=0.8),
            GraphRetrieval(store=graph_store, weight=0.7),
        ],
        top_k=8,
        cross_reference_enrichment=True,
    )

    generation = GenerationConfig(
        lm_client=_generation_client(),
        system_prompt=_OPERATION_SYSTEM_PROMPT,
        grounding_enabled=True,
        grounding_threshold=0.4,
    )

    routing = RoutingConfig(
        mode=QueryMode.AUTO,
        full_context_threshold=_FULL_CONTEXT_THRESHOLD,
    )

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
