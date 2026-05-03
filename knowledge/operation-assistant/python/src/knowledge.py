"""KnowledgeEngine wiring for the operation-assistant.

This module's only job is to build a ``KnowledgeEngineConfig`` and hand the
resulting engine to FastAPI's lifespan. All vendor-touching code lives in
``providers.py`` — engine.py imports providers + stores from rfnry-knowledge
and composes them.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from rfnry_knowledge import (
    DrawingIngestion,
    DrawingIngestionConfig,
    EntityIngestion,
    EntityIngestionConfig,
    EntityRetrieval,
    GenerationConfig,
    IngestionConfig,
    KeywordIngestion,
    KeywordRetrieval,
    KnowledgeEngine,
    KnowledgeEngineConfig,
    Neo4jGraphStore,
    PostgresDocumentStore,
    QdrantVectorStore,
    QueryMode,
    RetrievalConfig,
    RoutingConfig,
    SemanticIngestion,
    SemanticRetrieval,
    SQLAlchemyMetadataStore,
    StructuredIngestion,
)

from src.providers import Settings, embeddings, generation_client, vision_client, vision_sentinel

OPERATION_SYSTEM_PROMPT = (
    "You are a factory operations assistant. Use only the provided context — extracted "
    "from machine manuals and mechanical drawings — to answer technician questions. "
    "Cite source ids and page numbers. Reference specific components, wiring connections, "
    "and procedure steps. If the context does not contain the answer, say so plainly."
)


def build_config(settings: Settings) -> KnowledgeEngineConfig:
    embedder = embeddings(settings)
    embedding_model_name = f"{embedder.name}:{embedder.model}"

    gen_client = generation_client(settings)
    vis_client = vision_client(settings)
    vis_sentinel = vision_sentinel()

    vector_store = QdrantVectorStore(
        url=settings.qdrant_url,
        collection=settings.qdrant_collection,
    )
    metadata_store = SQLAlchemyMetadataStore(url=settings.postgres_url)
    document_store = PostgresDocumentStore(url=settings.postgres_url)
    graph_store = Neo4jGraphStore(
        uri=settings.neo4j_url,
        username=settings.neo4j_user,
        password=settings.neo4j_password,
    )

    entity_config = EntityIngestionConfig(
        relationship_keyword_map={
            "connected": "CONNECTS_TO",
            "wired": "CONNECTS_TO",
            "feeds": "FEEDS",
            "controls": "CONTROLLED_BY",
            "mounted": "REFERENCES",
        },
        unclassified_relation_default="MENTIONS",
    )

    ingestion = IngestionConfig(
        methods=[
            SemanticIngestion(
                store=vector_store,
                embeddings=embedder,
                embedding_model_name=embedding_model_name,
            ),
            KeywordIngestion(store=document_store),
            EntityIngestion(
                store=graph_store,
                provider_client=vis_client,
                graph_config=entity_config,
            ),
            StructuredIngestion(
                store=vector_store,
                embeddings=embedder,
                vision=vis_sentinel,
                provider_client=vis_client,
                graph_store=graph_store,
                embedding_model_name=embedding_model_name,
                analyze_concurrency=5,
                graph_config=entity_config,
            ),
            DrawingIngestion(
                config=DrawingIngestionConfig(
                    enabled=True,
                    provider_client=vis_client,
                    dpi=400,
                    analyze_concurrency=3,
                ),
                store=vector_store,
                embeddings=embedder,
                vision=vis_sentinel,
                provider_client=vis_client,
                graph_store=graph_store,
                embedding_model_name=embedding_model_name,
            ),
        ],
        chunk_size=375,
        chunk_overlap=40,
    )

    retrieval = RetrievalConfig(
        methods=[
            # Semantic pillar — dense embeddings over the vector store
            SemanticRetrieval(store=vector_store, embeddings=embedder, weight=1.0),
            # Keyword pillar — Postgres FTS over the document store
            KeywordRetrieval(backend="postgres_fts", document_store=document_store, weight=0.8),
            # Entity pillar — N-hop traversal over the graph store
            EntityRetrieval(store=graph_store, weight=0.7),
        ],
        top_k=8,
    )

    generation = GenerationConfig(
        provider_client=gen_client,
        system_prompt=OPERATION_SYSTEM_PROMPT,
        grounding_enabled=True,
        grounding_threshold=0.4,
    )

    routing = RoutingConfig(
        mode=QueryMode.AUTO,
        full_context_threshold=settings.full_context_threshold,
    )

    return KnowledgeEngineConfig(
        ingestion=ingestion,
        generation=generation,
        retrieval=retrieval,
        routing=routing,
        metadata_store=metadata_store,
    )


@asynccontextmanager
async def lifespan_engine() -> AsyncIterator[KnowledgeEngine]:
    settings = Settings.from_env()
    engine = KnowledgeEngine(build_config(settings))
    async with engine:
        yield engine
