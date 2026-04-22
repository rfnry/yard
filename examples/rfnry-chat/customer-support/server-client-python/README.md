# customer-support — server + agent

One FastAPI process:

- **Chat server** (`chat.py`) — `ChatServer` with `InMemoryChatStore`. Logs every message.
- **Agent** (`agent/`) — an `AssistantIdentity` that connects through `rfnry-chat-client` and answers user messages via Anthropic.

Everything runs in the same process for convenience. The agent is still a regular chat client, so in production the two halves split cleanly.

## Layout

```
src/
  main.py              FastAPI app + lifespan — starts chat_server, schedules the agent
  chat.py              ChatServer + message logger
  agent/
    client.py          ChatClient lifecycle — connect, retry, register the handler
    assistant.py       (ctx, send) handler: history → Anthropic → reply
    provider.py        Anthropic SDK glue
```

## Run

```bash
cd yard/examples/rfnry-chat/customer-support/server-client-python
cp .env.example .env    # then fill in ANTHROPIC_API_KEY (optional — stubs if unset)
uv sync --extra dev

uv run poe dev          # hot-reload dev server (recommended)
uv run poe start        # same, without --reload
```

No DB, no auth — identity comes from the `x-rfnry-identity` header the client auto-encodes. Every server restart wipes state.

## Development

Dev tooling via [`poethepoet`](https://poethepoet.natn.io/) (tasks declared in `pyproject.toml`, `[tool.poe.tasks]`).

```bash
uv sync --extra dev           # install ruff + mypy + poethepoet

uv run poe dev                # start dev server with --reload
uv run poe start              # start server (no reload)
uv run poe format             # ruff format .
uv run poe format:imports     # ruff check --select I --fix .
uv run poe check              # ruff check .
uv run poe check:fix          # ruff check --fix .
uv run poe typecheck          # mypy src
```
