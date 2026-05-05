# travel-planner — server-client-python

FastAPI server wrapping a rfnry `AgentEngine` that runs the `plan-trip` workflow.

## Setup

```bash
cd server-client-python
uv sync
export ANTHROPIC_API_KEY=...           # required
export ANTHROPIC_MODEL=claude-sonnet-4-6  # optional override
```

## Run

```bash
uv run poe dev
# server listens on :8105
```

## Plan a trip

```bash
curl -X POST http://localhost:8105/plan-trip \
  -H 'content-type: application/json' \
  -d '{
    "session_id": "trip-001",
    "traveler_id": "alice",
    "origin": "JFK",
    "destination": "Lisbon",
    "arrival_date": "2026-09-12",
    "departure_date": "2026-09-19",
    "travelers": 2,
    "mood": "cultural",
    "budget_band": "mid-range"
  }'
```

The response is a validated `TripPlan` (see `src/schemas.py`).

## Resume after crash

The workflow event log lives at
`agents/data/<traveler_id>/workflows/plan-trip/<session_id>/events.jsonl`.
If a step fails (e.g. one scout's stub URL is unreachable), the same
session can be resumed:

```bash
curl -X POST http://localhost:8105/plan-trip/resume \
  -H 'content-type: application/json' \
  -d '{"session_id": "trip-001", "traveler_id": "alice"}'
```

The executor replays the namespace from completed-step events and
re-runs only what didn't finish. Note: the **`parallel:` block is
all-or-nothing on resume in v1** — if one of the four scouts didn't
complete, all four re-run.

## What's inside

```
src/
├── engine.py        # AgentEngine + OutputSchemas wiring
├── schemas.py       # Pydantic classes for every scout output + TripPlan
├── provider.py      # Anthropic adapter (per-member)
├── routes.py        # POST /plan-trip + /plan-trip/resume
└── server.py        # FastAPI entrypoint

agents/
├── WORKFLOW.md      # plan-trip: parallel { 4 scouts } → synthesizer
├── flight-scout/
├── hotel-scout/
├── activity-curator/
├── weather-watcher/
└── trip-synthesizer/
```

## Per-traveler scope

`namespaces=["traveler_id"]`. Every turn's data partitions under
`agents/data/<traveler_id>/...`. The path-jail blocks cross-traveler
reads structurally, even under prompt injection. Reflections and
lessons accumulate per-traveler-per-task — `find-flights` lessons
that work for one traveler don't leak to another's boot bundle.

## Telemetry

```bash
sqlite3 agents/data/alice/state.db.telemetry "select task, provider_calls, duration_ms from turns order by id desc limit 10;"
```

Every scout turn is one row; the workflow's synthesize step is another.
The host applies its own rate card to compute cost from token totals
— rfnry never embeds pricing.
