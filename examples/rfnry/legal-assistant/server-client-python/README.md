# legal-assistant — server

Two clean layers:

- `src/main.py` — FastAPI bootstrap (HTTP infra only).
- `src/app.py` — Agent construction (application layer); the
  `AnthropicProvider` is built inline from `ANTHROPIC_API_KEY`
  (required — boot raises `KeyError` if unset).
- `src/routes.py` — `POST /turn`, `POST /resume`, `GET /health`.

The agent declares `namespaces=["case_id"]`. Every request supplies
a `case_id` in the body, which rfnry validates into a single-segment
path leaf. Per-case data lives at `agent/data/<case_id>/...` and the
path-jail blocks any read/write outside it.

## Endpoints

```
POST /turn       { "session_id":"...", "case_id":"...", "message":"...", "task":"investigate" }
POST /resume     { "session_id":"...", "case_id":"..." }
GET  /health
```

## Run

```bash
# terminal 1: backend
cd yard/examples/rfnry/backend
uv sync --extra dev
uv run poe dev          # http://127.0.0.1:8200

# terminal 2: agent
cd yard/examples/rfnry/legal-assistant/server-client-python
cp .env.example .env
uv sync --extra dev
uv run poe dev          # http://127.0.0.1:8102
```

## Drive a turn

```bash
curl -X POST http://localhost:8102/turn \
  -H 'content-type: application/json' \
  -d '{
    "session_id": "intake-1",
    "case_id": "case-2026-CIV-0042",
    "task": "investigate",
    "message": "Client wants me to evaluate a witness named ID-9876. Pull what we have on identity, criminal history, and property records — note anything that bears on credibility."
  }'
```

## Two cases, isolated

```bash
# case-A turn
curl -X POST http://localhost:8102/turn -H 'content-type: application/json' \
  -d '{"session_id":"a-1","case_id":"case-A","message":"...","task":"investigate"}'

# case-B turn  
curl -X POST http://localhost:8102/turn -H 'content-type: application/json' \
  -d '{"session_id":"b-1","case_id":"case-B","message":"...","task":"investigate"}'
```

State partitions:

```
data/case-A/sessions/a-1/events.jsonl
data/case-A/state.db                      # case-A's lessons + reflections
data/case-A/tasks/investigate/...         # per-task accumulator state
data/case-B/sessions/b-1/events.jsonl
data/case-B/state.db                      # case-B's lessons + reflections
data/case-B/tasks/investigate/...
```

The `case-B` agent never sees `case-A`'s lessons — they don't enter
the boot bundle, and even if a tool tried to read across, the path-
jail rejects it.

## Refining (the point of this example)

This example leans on rfnry's refining loop:

```bash
uv run rfnry inspect lessons ./agent --scope case_id=case-A --task investigate
uv run rfnry inspect sessions ./agent --scope case_id=case-A
```

After a few turns within one case, run consolidation (via the
`Agent.consolidate` API or by adding more turns and triggering on a
schedule) to distill the recurring patterns into per-case lessons
that load into the next boot bundle. Other cases remain unaffected.
