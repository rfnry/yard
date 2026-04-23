# stock-assistant — agent + webhook

Standalone agent that connects to the chat server at `http://127.0.0.1:8000` and serves an `/alert-user` webhook on port `9100`.

- When a user talks in a thread the agent is a member of, it answers via Anthropic.
- When something hits `/alert-user`, the agent proactively opens (or reuses) a thread with that user and sends them a message. This is the "inverted flow" — the agent reaches out first.

## Layout

```
src/
  main.py      FastAPI app — lifespan runs the ChatClient, `/alert-user` webhook
  agent.py     identity + @on_message handler
  provider.py  Anthropic SDK glue
```

## Run

```bash
# Prereq: the chat server is up on :8000 (see ../server-python/README.md).

cd yard/examples/rfnry-chat/stock-assistant/client-python
cp .env.example .env    # then fill in ANTHROPIC_API_KEY (optional), CHAT_SERVER_URL, PORT
uv sync --extra dev

uv run poe dev          # hot-reload dev server on :9100 (recommended)
uv run poe start        # same, without --reload
```

## Trigger a proactive alert

```bash
# Brand new thread for user u_alice:
curl -X POST http://localhost:9100/alert-user \
  -H "content-type: application/json" \
  -d '{"user_id": "u_alice", "message": "AAPL broke 200 — want a read?"}'

# Continue in an existing thread:
curl -X POST http://localhost:9100/alert-user \
  -H "content-type: application/json" \
  -d '{"user_id": "u_alice", "thread_id": "th_...", "message": "Update: it just pulled back to 198."}'
```

Response: `{"thread_id": "th_...", "event_id": "evt_..."}`.

## Development

Dev tooling via [`poethepoet`](https://poethepoet.natn.io/) (tasks declared in `pyproject.toml`, `[tool.poe.tasks]`).

```bash
uv sync --extra dev           # install ruff + mypy + poethepoet

uv run poe dev                # start dev server with --reload (port 9100)
uv run poe start              # start server (no reload)
uv run poe format             # ruff format .
uv run poe format:imports     # ruff check --select I --fix .
uv run poe check              # ruff check .
uv run poe check:fix          # ruff check --fix .
uv run poe typecheck          # mypy src
```
