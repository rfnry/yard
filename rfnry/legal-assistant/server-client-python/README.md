# legal-assistant — server

Layout:

```
server-client-python/
├── agent/              the markdown tree the model navigates (AGENT.md, rules/, skills/, tools/, tasks/)
└── src/
    ├── main.py         FastAPI infra
    ├── routes.py       HTTP routes — Pydantic + HTTP↔agent.* binding
    └── agent/          the Python application layer
        ├── server.py   `agent = AgentEngine(...)` — module-level binding
        ├── turn.py     run_turn
        ├── resume.py   run_resume
        └── consolidate.py  run_consolidate
```

Two things named `agent/` here, two different things:

- `server-client-python/agent/` — the **markdown tree the model
  navigates** (AGENT.md, rules/, skills/, tools/, tasks/). Edit on
  GitHub; no Python required to author.
- `server-client-python/src/agent/` — the **Python application
  layer** that wraps the engine. `server.py` builds the
  `rfnry.Agent` (with inline `AnthropicProvider` from
  `ANTHROPIC_API_KEY`, required — boot raises `KeyError` if unset);
  `turn.py` / `resume.py` / `consolidate.py` orchestrate
  per-request flows; `__init__.py` re-exports `run_turn`,
  `run_resume`, and `run_consolidate` so `routes.py` calls them
  directly.

`src/main.py` is HTTP infra only (FastAPI, CORS, uvicorn). `src/routes.py`
is Pydantic models + HTTPException shaping for `POST /turn`,
`POST /resume`, `POST /consolidate`, `GET /health`.

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
data/case-A/state.db                                # case-A's lessons + reflections (sqlite mirror)
data/case-A/refining/reflections/investigate/...    # per-turn reflections
data/case-A/refining/outcomes/investigate/...       # per-turn critic outcomes
data/case-A/refining/lessons/investigate/...        # consolidated lessons (boot bundle)
data/case-A/refining/eval/investigate/cases/...     # eval cases (used by GEPA + lesson gate)
data/case-A/refining/optimizations/skills/<skill>/<run_id>/...   # GEPA runs
data/case-B/...                                     # fully isolated mirror
```

The `case-B` agent never sees `case-A`'s lessons — they don't enter
the boot bundle, and even if a tool tried to read across, the path-
jail rejects it.

## Refining (the point of this example)

This example exercises both rfnry refining cadences plus typed task output:

1. **Reflection → lesson (tasks-only).** Per-turn reflections + critic
   outcomes accumulate under `data/<case_id>/refining/{reflections,outcomes}/<task>/`.
   `POST /consolidate` clusters them into eval-gated lessons that land in the
   next boot bundle. Configured via `RefiningTasksConfig` in `server.py`.
2. **GEPA optimization (any surface).** `POST /optimize/skill` runs
   `Agent.optimize_method("skills", ...)` against a single skill markdown,
   producing a destructive edit to `agent/skills/<skill>.md` gated by the
   eval suite for that case + task. Configured via
   `RefiningSkillsConfig(optimize=GEPAOptimizeConfig(budget="small"))`.
3. **Structured reply (`output_schemas`).** The engine wires
   `output_schemas=OutputSchemas(tasks={"investigate": InvestigationReport})`.
   The harness synthesizes a terminal `OutputSchema` tool whose
   input_schema is the Pydantic class's JSON schema; the model fills
   it in at end of turn and the server returns the validated dict.
   See `src/schemas.py` for the shape and `src/engine.py` for
   `agent_engine.turn(..., expect=InvestigationReport)`.

Inspect persisted state:

```bash
uv run rfnry inspect lessons ./agent --scope case_id=case-A --task investigate
uv run rfnry inspect sessions ./agent --scope case_id=case-A
```

GEPA needs eval cases on disk under
`data/<case_id>/refining/eval/<task>/cases/`. Cases are extracted from
low-quality outcomes via `Agent.extract_eval_case` after enough turns,
or curated by the operator. Without cases, `/optimize/skill` returns
`EvaluationError: optimize_method requires at least one EvalCase`.
