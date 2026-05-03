from __future__ import annotations

import os

from pydantic import SecretStr
from rfnry_chat_client import ChatClient, HandlerContext, Send
from rfnry_chat_client.providers import (
    AnthropicConfig,
    MockConfig,
    TextMessages,
    events_to_messages,
    last_user_text,
    resolve_text_messages,
)
from rfnry_chat_protocol import AssistantIdentity, Identity, TextPart

ORGANIZATION = "organization-a"
ASSISTANT_ID = "agent-a"
ASSISTANT_NAME = "Agent A"

IDENTITY = AssistantIdentity(
    id=ASSISTANT_ID,
    name=ASSISTANT_NAME,
    metadata={"tenant": {"organization": ORGANIZATION, "workspace": "*", "author": "*"}},
)

SYSTEM_PROMPT = (
    "You are Agent A, the assistant for organization-a. "
    "You serve both workspaces in this organization (workspace-a-1 and workspace-a-2). "
    "Be concise and address the requester by name when appropriate. "
    "Mention which workspace the question came from when it seems useful."
)


def build_provider() -> TextMessages:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("ANTHROPIC_API_KEY unset — provider stubbed via MockConfig")
        return resolve_text_messages(MockConfig(model="mock-claude"))
    return resolve_text_messages(
        AnthropicConfig(api_key=SecretStr(api_key), model="claude-sonnet-4-5-20250929")
    )


def register(client: ChatClient) -> None:
    provider = build_provider()

    @client.on_message()
    async def respond(ctx: HandlerContext, send: Send):
        author = ctx.event.author

        history_page = await client.rest.list_events(ctx.event.thread_id, limit=200)
        history = history_page["items"]
        messages = events_to_messages(history, self_id=IDENTITY.id)
        if not messages:
            return

        system_prompt = f"{SYSTEM_PROMPT}\n\n{_requester_context(author)}"

        if provider.kind == "mock":
            yield send.message(
                content=[
                    TextPart(
                        text=(
                            f"[stub reply from {IDENTITY.name} — set ANTHROPIC_API_KEY "
                            f"to wire the real model] you said: "
                            f"{last_user_text(history, self_id=IDENTITY.id)}"
                        )
                    )
                ]
            )
            return

        reply = await provider.generate(system=system_prompt, messages=messages, tools=[])
        if reply.text:
            yield send.message(content=[TextPart(text=reply.text)])


def _requester_context(author: Identity) -> str:
    metadata = author.metadata or {}
    tenant_raw = metadata.get("tenant")
    tenant = tenant_raw if isinstance(tenant_raw, dict) else {}
    organization = tenant.get("organization") or "unknown"
    workspace = tenant.get("workspace") or "unknown"
    return (
        f"The current requester is {author.name} (id={author.id}) "
        f"from organization={organization} in workspace={workspace}."
    )
