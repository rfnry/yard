# team-communication — chat server

Standalone `rfnry-chat-server` with an `InMemoryChatStore`, shaped as a small Slack-style demo. Pre-creates two channel threads (`ch_general`, `ch_engineering`) at startup; DMs are created on demand by clients.

Uses a hybrid `authorize` callback (`src/chat.py`): channel threads are public (anyone authenticated can read/post), DM threads are member-only. A small REST route override hides DM threads from non-members in `GET /threads` listings so users only see DMs they belong to. See [`../README.md`](../README.md) for the conceptual model and role matrix.

## Layout

- `src/main.py` — server entrypoint, pre-seeds channel threads
- `src/chat.py` — hybrid `authorize` + DM-filter route override
- `src/__init__.py` — package marker

## Run

```bash
cd yard/examples/rfnry-chat/team-communication/server-python
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

## Example vs library

Both the hybrid `authorize` callback and the DM-filter route override live in **this example**, not in `rfnry-chat-server`. They're example-specific access twists (channels public, DMs private) — the library stays general and exposes the hooks this example plugs into.
