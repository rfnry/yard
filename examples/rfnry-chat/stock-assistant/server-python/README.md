# stock-assistant — chat server

Standalone `rfnry-chat-server` with an `InMemoryChatStore`. The stock-assistant agent (`../client-python`) connects as an external participant and also hosts the `/alert-user` webhook.

## Run

```bash
cd yard/examples/rfnry-chat/stock-assistant/server-python
cp .env.example .env    # optional — only PORT override lives here
uv sync --extra dev

uv run poe dev          # hot-reload dev server (recommended)
uv run poe start        # same, without --reload
```

No auth, no DB. State vanishes on restart.

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
