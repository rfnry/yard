from __future__ import annotations

from pydantic import SecretStr
from rfnry_knowledge import BaseEmbeddings, EmbeddingResult, ProviderClient, TokenUsage
from rfnry_knowledge.ingestion.models import ParsedPage
from rfnry_knowledge.ingestion.vision.base import BaseVision

from src.settings import Settings


def generation_client(settings: Settings) -> ProviderClient:
    return ProviderClient(
        name="anthropic",
        model=settings.generation_model,
        api_key=SecretStr(settings.anthropic_api_key),
        max_tokens=4096,
        temperature=0.0,
        context_size=200_000,
    )


def vision_client(settings: Settings) -> ProviderClient:
    return ProviderClient(
        name="anthropic",
        model=settings.vision_model,
        api_key=SecretStr(settings.anthropic_api_key),
        max_tokens=4096,
        temperature=0.0,
    )


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


class _BAMLOnlyVision:
    async def parse(self, file_path: str, pages: set[int] | None = None) -> list[ParsedPage]:
        raise NotImplementedError(
            f"vision.parse({file_path!r}) called: this assistant only ingests PDFs and plain "
            "markdown, which are handled via BAML directly. Add a real BaseVision impl to "
            "providers.py if you start ingesting raw image files (.jpg/.png/.webp)."
        )


def vision_sentinel() -> BaseVision:
    return _BAMLOnlyVision()
