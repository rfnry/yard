from __future__ import annotations

import os
from typing import Any

from rfnry.host.protocol import Message, ProviderReply, ToolSpec


def build_provider() -> Any:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("ANTHROPIC_API_KEY unset — using stub provider (echoes user message)")
        return _StubProvider()
    from anthropic import AsyncAnthropic

    from rfnry.providers.anthropic import AnthropicProvider

    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    return AnthropicProvider(client=AsyncAnthropic(api_key=api_key), model=model)


class _StubProvider:
    async def generate(
        self,
        system: str,
        messages: list[Message],
        tools: list[ToolSpec],
    ) -> ProviderReply:
        last_user = next(
            (m.content for m in reversed(messages) if m.role == "user" and isinstance(m.content, str)),
            "",
        )
        return ProviderReply(
            text=f"[stub] you asked: {last_user[:120]}",
            stop_reason="end_turn",
            tool_calls=[],
        )
