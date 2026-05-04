from __future__ import annotations

import os
from dataclasses import dataclass

from anthropic import AsyncAnthropic
from pydantic import SecretStr
from rfnry_knowledge import BaseEmbeddings, EmbeddingResult, ProviderClient, TokenUsage


def _require(env: str) -> str:
    value = os.environ.get(env, "").strip()
    if not value:
        raise RuntimeError(f"{env} must be set")
    return value


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    anthropic_api_key: str
    embedding_model: str
    chat_model: str
    qdrant_url: str
    qdrant_collection: str

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            openai_api_key=_require("OPENAI_API_KEY"),
            anthropic_api_key=_require("ANTHROPIC_API_KEY"),
            embedding_model=os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small"),
            chat_model=os.environ.get("CHAT_MODEL", "claude-sonnet-4-5"),
            qdrant_url=os.environ.get("QDRANT_URL", "http://localhost:6333"),
            qdrant_collection=os.environ.get("QDRANT_COLLECTION", "therapy-assistant"),
        )


def extractor_provider(settings: Settings) -> ProviderClient:
    return ProviderClient(
        name="anthropic",
        model=settings.chat_model,
        api_key=SecretStr(settings.anthropic_api_key),
        max_tokens=2048,
        temperature=0.0,
    )


def chat_client(settings: Settings) -> AsyncAnthropic:
    return AsyncAnthropic(api_key=settings.anthropic_api_key)


class OpenAIEmbeddings:
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
