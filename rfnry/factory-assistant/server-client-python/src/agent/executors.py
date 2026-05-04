from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from typing import Any

from rfnry_knowledge import KnowledgeEngine

from src.settings import Settings

KnowledgeExecutor = Callable[[dict[str, Any]], Awaitable[str]]


def build_knowledge_executor(engine: KnowledgeEngine, settings: Settings) -> KnowledgeExecutor:
    async def knowledge_query(input: dict[str, Any]) -> str:
        query = (input.get("query") or "").strip()
        if not query:
            return json.dumps({"error": "missing 'query'"})
        knowledge_id = (input.get("knowledge_id") or settings.knowledge_id).strip()

        result = await engine.query(text=query, knowledge_id=knowledge_id, trace=True)
        trace = result.trace
        sources = [
            {
                "source_id": s.source_id,
                "page_number": s.page_number,
                "score": round(s.score, 4),
            }
            for s in result.sources
        ]
        return json.dumps(
            {
                "answer": result.answer or "",
                "routing": trace.routing_decision if trace else None,
                "grounding": trace.grounding_decision if trace else None,
                "sources": sources,
            },
            ensure_ascii=False,
        )

    return knowledge_query
