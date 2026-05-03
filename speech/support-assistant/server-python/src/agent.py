from __future__ import annotations

import os

from openai import AsyncOpenAI
from rfnry_voice_server.providers.openai.sts import OpenAISTSProvider
from rfnry_voice_server.session import VoiceSession
from rfnry_voice_server.transport.protocols import Transport

from src.tools import TOOLS

INSTRUCTIONS = """You are a friendly, concise rental car support agent.
Speak naturally and never robotically. Keep responses short — 1 to 2 sentences
unless the caller asks for detail. You may use the available tools to look up
accounts, list rentals, refund a rental, or escalate. Confirm refunds verbally
before issuing them. If you cannot help, escalate.
"""


def build_sts_provider() -> OpenAISTSProvider:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY env var is required")
    client = AsyncOpenAI(api_key=api_key)
    return OpenAISTSProvider(
        client=client,
        model=os.environ.get("OPENAI_REALTIME_MODEL", "gpt-realtime"),
        instructions=INSTRUCTIONS,
    )


def make_session(
    *,
    session_id: str,
    transport: Transport,
) -> VoiceSession:
    sts = build_sts_provider()
    return VoiceSession(
        namespaces=["org_id"],
        scope={"org_id": "support-assistant"},
        transport=transport,
        sts=sts,
        tools=TOOLS,
        session_id=session_id,
    )
