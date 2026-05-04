from __future__ import annotations

import time
from typing import Any, cast

from anthropic import AsyncAnthropic
from rfnry.exceptions import ConfigurationError
from rfnry.host.protocol import Message, ProviderReply, ToolCall, ToolSpec

_STOP_MAP: dict[str, str] = {
    "end_turn": "end_turn",
    "tool_use": "tool_use",
    "max_tokens": "max_tokens",
    "stop_sequence": "end_turn",
}


class AnthropicProvider:
    def __init__(
        self,
        client: AsyncAnthropic,
        model: str,
        max_tokens: int = 4096,
    ) -> None:
        if not model:
            raise ConfigurationError("AnthropicProvider requires a non-empty model name")
        self.client = client
        self.model = model
        self.max_tokens = max_tokens

    async def generate(
        self,
        system: str,
        messages: list[Message],
        tools: list[ToolSpec],
    ) -> ProviderReply:
        system_blocks: list[dict[str, Any]] = [
            {
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral"},
            }
        ]
        remaining = messages
        if remaining and remaining[0].role == "system":
            tail_content = remaining[0].content
            if isinstance(tail_content, str):
                system_blocks.append({"type": "text", "text": tail_content})
            remaining = remaining[1:]

        wire_messages = [_to_wire(m) for m in remaining]
        tool_catalog = [_tool_to_wire(t) for t in tools]
        started = time.monotonic()
        resp = await self.client.messages.create(
            model=self.model,
            system=cast(Any, system_blocks),
            messages=cast(Any, wire_messages),
            tools=cast(Any, tool_catalog),
            max_tokens=self.max_tokens,
        )
        duration_ms = int((time.monotonic() - started) * 1000)
        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []
        for block in resp.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.id,
                        name=block.name,
                        args=dict(block.input) if block.input else {},
                    )
                )
        usage_obj = resp.usage
        return ProviderReply(
            text="".join(text_parts),
            tool_calls=tool_calls,
            usage={
                "input": usage_obj.input_tokens,
                "output": usage_obj.output_tokens,
                "cache_creation": getattr(usage_obj, "cache_creation_input_tokens", 0) or 0,
                "cache_read": getattr(usage_obj, "cache_read_input_tokens", 0) or 0,
            },
            stop_reason=_STOP_MAP.get(resp.stop_reason or "end_turn", "end_turn"),  # type: ignore[arg-type]
            provider="anthropic",
            model=self.model,
            duration_ms=duration_ms,
        )


def _tool_to_wire(tool: ToolSpec) -> dict[str, Any]:
    return {
        "name": tool.name,
        "description": tool.description,
        "input_schema": tool.input_schema,
    }


def _to_wire(msg: Message) -> dict[str, Any]:
    if msg.role == "tool":
        return {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": msg.tool_call_id or "",
                    "content": msg.content if isinstance(msg.content, str) else "",
                }
            ],
        }
    return {"role": msg.role, "content": msg.content}
