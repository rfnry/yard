# team-communication — Agent C (Support Liaison)

Agent process for the `team-communication` demo. Connects to the chat server at `http://127.0.0.1:8000` and serves two webhooks on port `9102`:

- `POST /ping-channel` — stream a persona-appropriate opener into a given channel thread.
- `POST /ping-direct`  — open-or-reuse a DM with a given user and stream an opener into it.

See [`../README.md`](../README.md) for the full model, the sibling agents (A, B), and the seven-step verification checklist.

## Layout

```
src/
  main.py        FastAPI app — ChatClient lifespan + /ping-channel + /ping-direct webhooks
  agent.py       AssistantIdentity + persona prompt (Support Liaison)
  provider.py    Anthropic SDK glue (streams tokens; stubs out if ANTHROPIC_API_KEY is unset)
  topics.py      mock "subject" pool used to seed each proactive ping
```

## Run

```bash
# Prereq: chat server is up on :8000 (see ../server-python/README.md).

cd yard/examples/rfnry-chat/team-communication/client-python-c
cp .env.example .env    # optional — ANTHROPIC_API_KEY, CHAT_SERVER_URL, PORT
uv sync --extra dev

uv run poe dev          # hot-reload dev server on :9102 (recommended)
uv run poe start        # same, without --reload
```

## Development

Dev tooling via [`poethepoet`](https://poethepoet.natn.io/) (tasks declared in `pyproject.toml`, `[tool.poe.tasks]`).

```bash
uv run poe dev                # start dev server with --reload (port 9102)
uv run poe start              # start server (no reload)
uv run poe format             # ruff format .
uv run poe check              # ruff check .
uv run poe typecheck          # mypy src
```
