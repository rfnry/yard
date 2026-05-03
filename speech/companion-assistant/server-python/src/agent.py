from __future__ import annotations

import os

from openai import AsyncOpenAI
from rfnry_voice_server.providers.openai.sts import OpenAISTSProvider
from rfnry_voice_server.session import VoiceSession
from rfnry_voice_server.transport.protocols import Transport

from src.memory import CompanionContext, CompanionMemory

SYSTEM_PROMPT_TEMPLATE = """You are {companion_name}, a warm, curious voice companion talking with {user_name}.

Speak naturally. Never robotic. Take initiative — ask follow-ups, share observations, sometimes shift the subject. You are voice-only: no markdown, no lists, no formatting. Keep responses short unless {user_name} asks for more.

{summary_section}

{history_section}
"""


def _format_summary(summary: str) -> str:
    if not summary:
        return "Summary so far: (no prior conversation summary)."
    return f"Summary so far: {summary}"


def _format_history(ctx: CompanionContext) -> str:
    if not ctx.recent_turns:
        return "Recent turns: (no prior conversation yet)."
    lines = ["Recent turns:"]
    for turn in ctx.recent_turns:
        speaker = ctx.name if turn.speaker_id == "user" else "you"
        lines.append(f"- {speaker}: {turn.text}")
    return "\n".join(lines)


def build_instructions(*, companion_name: str, ctx: CompanionContext) -> str:
    return SYSTEM_PROMPT_TEMPLATE.format(
        companion_name=companion_name,
        user_name=ctx.name,
        summary_section=_format_summary(ctx.summary),
        history_section=_format_history(ctx),
    )


def build_sts_provider(*, instructions: str) -> OpenAISTSProvider:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY env var is required")
    client = AsyncOpenAI(api_key=api_key)
    return OpenAISTSProvider(
        client=client,
        model=os.environ.get("OPENAI_REALTIME_MODEL", "gpt-realtime"),
        instructions=instructions,
    )


def make_session(
    *,
    user_name: str,
    memory: CompanionMemory,
    transport: Transport,
    companion_name: str = "Sam",
) -> VoiceSession:
    ctx = memory.get(user_name)
    instructions = build_instructions(companion_name=companion_name, ctx=ctx)
    sts = build_sts_provider(instructions=instructions)
    return VoiceSession(
        namespaces=["user_id"],
        scope={"user_id": user_name},
        transport=transport,
        sts=sts,
    )
