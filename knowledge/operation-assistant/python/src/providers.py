"""Consumer-owned provider implementations.

`rfnry-knowledge` is provider-agnostic: it defines Protocols (BaseEmbeddings,
BaseVision, etc.) and a ProviderClient dataclass, then expects the host to
plug in concrete implementations. This module is where the operation-assistant
example does that plug-in. The engine should import only from here when it
needs anything that talks to a vendor.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from pydantic import SecretStr
from rfnry_knowledge import BaseEmbeddings, EmbeddingResult, ProviderClient, TokenUsage
from rfnry_knowledge.ingestion.models import ParsedPage
from rfnry_knowledge.ingestion.vision.base import BaseVision


def _require(env: str) -> str:
    value = os.environ.get(env, "").strip()
    if not value:
        raise RuntimeError(f"{env} must be set")
    return value


@dataclass(frozen=True)
class Settings:
    """Resolved environment for the assistant. Read once at startup."""

    openai_api_key: str
    anthropic_api_key: str
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
            openai_api_key=_require("OPENAI_API_KEY"),
            anthropic_api_key=_require("ANTHROPIC_API_KEY"),
            embedding_model=os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small"),
            generation_model=os.environ.get("GENERATION_MODEL", "claude-sonnet-4-5"),
            vision_model=os.environ.get("VISION_MODEL", "claude-sonnet-4-5"),
            qdrant_url=os.environ.get("QDRANT_URL", "http://localhost:6333"),
            qdrant_collection=os.environ.get("QDRANT_COLLECTION", "operation-assistant"),
            postgres_url=_require("POSTGRES_URL"),
            neo4j_url=os.environ.get("NEO4J_URL", "bolt://localhost:7687"),
            neo4j_user=os.environ.get("NEO4J_USER", "neo4j"),
            neo4j_password=_require("NEO4J_PASSWORD"),
            knowledge_id=os.environ.get("KNOWLEDGE_ID", "machines"),
            full_context_threshold=int(os.environ.get("FULL_CONTEXT_THRESHOLD", "150000")),
        )


# ---------------------------------------------------------------------------
# Provider clients (BAML-routed: generation + drawing/page analysis)
# ---------------------------------------------------------------------------


def generation_client(settings: Settings) -> ProviderClient:
    """Anthropic ProviderClient for the answer-generation path and the relevance gate."""
    return ProviderClient(
        name="anthropic",
        model=settings.generation_model,
        api_key=SecretStr(settings.anthropic_api_key),
        max_tokens=4096,
        temperature=0.0,
        context_size=200_000,
    )


def vision_client(settings: Settings) -> ProviderClient:
    """Anthropic ProviderClient for AnalyzedIngestion + DrawingIngestion BAML calls."""
    return ProviderClient(
        name="anthropic",
        model=settings.vision_model,
        api_key=SecretStr(settings.anthropic_api_key),
        max_tokens=4096,
        temperature=0.0,
    )


# ---------------------------------------------------------------------------
# BaseEmbeddings — OpenAI dense embeddings
# ---------------------------------------------------------------------------


class OpenAIEmbeddings:
    """Minimal BaseEmbeddings impl backed by the OpenAI Python SDK."""

    def __init__(self, api_key: str, model: str) -> None:
        from openai import AsyncOpenAI

        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model
        self._dim: int | None = None

    @property
    def name(self) -> str:
        return "openai"

    @property
    def model(self) -> str:
        return self._model

    async def embed(self, texts: list[str]) -> EmbeddingResult:
        if not texts:
            return EmbeddingResult(vectors=[], usage=None)
        response = await self._client.embeddings.create(input=texts, model=self._model)
        vectors = [item.embedding for item in response.data]
        usage = TokenUsage(
            input=int(getattr(response.usage, "prompt_tokens", 0) or 0),
            output=0,
        )
        if self._dim is None and vectors:
            self._dim = len(vectors[0])
        return EmbeddingResult(vectors=vectors, usage=usage)

    async def embedding_dimension(self) -> int:
        if self._dim is not None:
            return self._dim
        sample = await self.embed(["dimension probe"])
        if not sample.vectors:
            raise RuntimeError("OpenAI embeddings returned no vectors for dimension probe")
        return len(sample.vectors[0])


def embeddings(settings: Settings) -> BaseEmbeddings:
    return OpenAIEmbeddings(api_key=settings.openai_api_key, model=settings.embedding_model)


# ---------------------------------------------------------------------------
# BaseVision — sentinel only
# ---------------------------------------------------------------------------
#
# AnalyzedIngestion + DrawingIngestion require a BaseVision-conforming object,
# but the actual per-page work is BAML-routed (AnalyzePage / AnalyzeDrawingPage)
# via vision_client(). The sentinel below satisfies the Protocol so init
# validation passes; .parse() is never called for PDF/DXF inputs.
#
# Replace with a real impl only if you start ingesting raw image files
# (.jpg/.png/.webp) — the IngestionService routes those through .parse()
# directly.


class _BAMLOnlyVision:
    async def parse(self, file_path: str, pages: set[int] | None = None) -> list[ParsedPage]:
        raise NotImplementedError(
            f"vision.parse({file_path!r}) called: this assistant only ingests PDFs/DXF, "
            "which are handled via BAML directly. Add a real BaseVision impl to providers.py "
            "if you need single-image (.jpg/.png/.webp) ingestion."
        )


def vision_sentinel() -> BaseVision:
    return _BAMLOnlyVision()
