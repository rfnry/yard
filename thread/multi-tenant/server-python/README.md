# multi-tenant — chat server

Standalone `rfnry-chat-server` with an `InMemoryChatStore`. No embedded agent — the two org-scoped agents (`../client-python-a`, `../client-python-b`) connect as external participants over sockets.

Uses a custom `authorize` callback (`src/chat.py`) that trusts tenant match as the full access decision — the "workspace is the room" pattern. See [`../README.md`](../README.md) for the conceptual model and role matrix.

## Run

```bash
cd yard/examples/rfnry-chat/multi-tenant/server-python
cp .env.example .env    # optional — only PORT override lives here
uv sync --extra dev

uv run poe dev          # hot-reload dev server (recommended)
uv run poe start        # same, without --reload
```

No auth, no DB — identity is taken from the `x-rfnry-identity` header the clients auto-encode. State vanishes on restart.

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
