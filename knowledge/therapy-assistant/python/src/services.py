from __future__ import annotations

from anthropic import AsyncAnthropic
from rfnry_knowledge import Interaction, InteractionTurn, MemoryEngine

from src.providers import Settings
from src.schemas import ChatResponse, RecalledMemory

SYSTEM_PROMPT = (
    "You are a warm, attentive therapy companion. You listen, reflect feelings back, "
    "ask gentle clarifying questions, and remember what the person has shared. "
    "If prior memories are provided, weave them in naturally rather than reciting them. "
    "Avoid clinical diagnoses; focus on the person's experience."
)


async def chat(
    *,
    engine: MemoryEngine,
    chat_client: AsyncAnthropic,
    memory_id: str,
    message: str,
    settings: Settings,
) -> ChatResponse:
    recalled = await engine.search(message, memory_id=memory_id, top_k=5)

    memory_block = "\n".join(f"- {r.row.text}" for r in recalled) or "(no prior memories)"
    system = f"{SYSTEM_PROMPT}\n\nWhat you remember about this person:\n{memory_block}"

    response = await chat_client.messages.create(
        model=settings.chat_model,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": message}],
    )
    reply = "".join(block.text for block in response.content if block.type == "text")

    await engine.add(
        Interaction(
            turns=(
                InteractionTurn(role="user", content=message),
                InteractionTurn(role="assistant", content=reply),
            ),
        ),
        memory_id=memory_id,
    )

    return ChatResponse(
        reply=reply,
        recalled=[RecalledMemory(text=r.row.text, score=r.score) for r in recalled],
    )
