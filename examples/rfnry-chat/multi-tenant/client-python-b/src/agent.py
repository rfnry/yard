from __future__ import annotations

from rfnry_chat_client import ChatClient, HandlerContext, Send
from rfnry_chat_protocol import AssistantIdentity, Identity, TextPart

from src import provider

ORGANIZATION = "organization-b"
ASSISTANT_ID = "agent-b"
ASSISTANT_NAME = "Agent B"

IDENTITY = AssistantIdentity(
    id=ASSISTANT_ID,
    name=ASSISTANT_NAME,
    metadata={"tenant": {"organization": ORGANIZATION, "workspace": "*", "author": "*"}},
)

SYSTEM_PROMPT = (
    "You are Agent B, the assistant for organization-b. "
    "You serve both workspaces in this organization (workspace-b-1 and workspace-b-2). "
    "Be concise and address the requester by name when appropriate. "
    "Mention which workspace the question came from when it seems useful."
)


def register(client: ChatClient) -> None:
    anthropic = provider.build_anthropic()

    @client.on_message()
    async def respond(ctx: HandlerContext, send: Send):
        author = ctx.event.author

        history_page = await client.rest.list_events(ctx.event.thread_id, limit=200)
        history = history_page["items"]
        messages = provider.to_anthropic_messages(history, IDENTITY.id)
        if not messages:
            return

        system_prompt = f"{SYSTEM_PROMPT}\n\n{_requester_context(author)}"

        if anthropic is None:
            yield send.message(
                content=[
                    TextPart(
                        text=(
                            f"[stub reply from {IDENTITY.name} — set ANTHROPIC_API_KEY "
                            f"to wire the real model] you said: "
                            f"{provider.last_user_text(history, IDENTITY.id)}"
                        )
                    )
                ]
            )
            return

        response = await provider.call(
            anthropic,
            messages=messages,
            system_prompt=system_prompt,
        )
        for block in response.content:
            text = getattr(block, "text", "")
            if getattr(block, "type", None) == "text" and text:
                yield send.message(content=[TextPart(text=text)])


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
