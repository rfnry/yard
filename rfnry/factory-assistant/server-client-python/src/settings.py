from __future__ import annotations

import os
from dataclasses import dataclass


def _require(env: str) -> str:
    value = os.environ.get(env, "").strip()
    if not value:
        raise RuntimeError(f"{env} must be set")
    return value


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str
    openai_api_key: str
    anthropic_model: str
    embedding_model: str
    generation_model: str
    vision_model: str
    qdrant_url: str
    qdrant_collection: str
    postgres_url: str
    neo4j_url: str
    neo4j_user: str
    neo4j_password: str
    knowledge_id: str
    full_context_threshold: int

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            anthropic_api_key=_require("ANTHROPIC_API_KEY"),
            openai_api_key=_require("OPENAI_API_KEY"),
            anthropic_model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
            embedding_model=os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small"),
            generation_model=os.environ.get("GENERATION_MODEL", "claude-sonnet-4-5"),
            vision_model=os.environ.get("VISION_MODEL", "claude-sonnet-4-5"),
            qdrant_url=os.environ.get("QDRANT_URL", "http://localhost:6333"),
            qdrant_collection=os.environ.get("QDRANT_COLLECTION", "factory-assistant"),
            postgres_url=_require("POSTGRES_URL"),
            neo4j_url=os.environ.get("NEO4J_URL", "bolt://localhost:7687"),
            neo4j_user=os.environ.get("NEO4J_USER", "neo4j"),
            neo4j_password=_require("NEO4J_PASSWORD"),
            knowledge_id=os.environ.get("KNOWLEDGE_ID", "factory"),
            full_context_threshold=int(os.environ.get("FULL_CONTEXT_THRESHOLD", "150000")),
        )
