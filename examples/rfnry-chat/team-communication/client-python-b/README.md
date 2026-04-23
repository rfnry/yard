# team-communication — Agent B (Release Coordinator)

Agent process for the `team-communication` demo. Connects to the chat server at `http://127.0.0.1:8000` and serves two webhooks on port `9101`:

- `POST /ping-channel` — stream a persona-appropriate opener into a given channel thread.
- `POST /ping-direct`  — open-or-reuse a DM with a given user and stream an opener into it.

See [`../README.md`](../README.md) for the full model, the sibling agents (A, C), and the seven-step verification checklist.

## Layout

```
src/
  main.py        FastAPI app — ChatClient lifespan + /ping-channel + /ping-direct webhooks
  agent.py       AssistantIdentity + persona prompt (Release Coordinator)
  provider.py    Anthropic SDK glue (streams tokens; stubs out if ANTHROPIC_API_KEY is unset)
  topics.py      mock "subject" pool used to seed each proactive ping
```

## Run

```bash
# Prereq: chat server is up on :8000 (see ../server-python/README.md).

cd yard/examples/rfnry-chat/team-communication/client-python-b
cp .env.example .env    # optional — ANTHROPIC_API_KEY, CHAT_SERVER_URL, PORT
uv sync --extra dev

uv run poe dev          # hot-reload dev server on :9101 (recommended)
uv run poe start        # same, without --reload
```

## Development

Dev tooling via [`poethepoet`](https://poethepoet.natn.io/) (tasks declared in `pyproject.toml`, `[tool.poe.tasks]`).

```bash
uv run poe dev                # start dev server with --reload (port 9101)
uv run poe start              # start server (no reload)
uv run poe format             # ruff format .
uv run poe check              # ruff check .
uv run poe typecheck          # mypy src
```
