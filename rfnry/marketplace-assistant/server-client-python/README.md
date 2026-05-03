# marketplace-assistant — server

Layout:

```
server-client-python/
├── agent/              the markdown tree the model navigates (AGENT.md, rules/, skills/, tools/, tasks/)
└── src/
    ├── main.py         FastAPI infra
    ├── routes.py       HTTP routes — Pydantic + HTTP↔agent.* binding
    └── agent/          the Python application layer
        ├── server.py   `agent = Agent(...)` — module-level binding
        ├── turn.py     run_turn
        └── resume.py   run_resume
```

Two things named `agent/` here, two different things:

- `server-client-python/agent/` — the **markdown tree the model
  navigates** (AGENT.md, rules/, skills/, tools/ — catalog, stock,
  orders, shipping, payments, promotions, sales-summary —
  tasks/team-lookup.md). Edit on GitHub; no Python required to
  author.
- `server-client-python/src/agent/` — the **Python application
  layer** that wraps the engine. `server.py` builds the
  `rfnry.Agent` (with inline `AnthropicProvider` from
  `ANTHROPIC_API_KEY`, required); `turn.py` / `resume.py` orchestrate
  per-request flows; `__init__.py` re-exports `run_turn` and
  `run_resume` so `routes.py` calls them directly.

`src/main.py` is HTTP infra only (FastAPI, CORS, uvicorn). `src/routes.py`
is Pydantic models + HTTPException shaping; the route bodies just await
`run_turn` / `run_resume`.

`ANTHROPIC_API_KEY` is required to start the server — there is no
stub fallback. Boot raises `KeyError` if it is unset.

## Endpoints

```
POST /turn       { "session_id":"...", "message":"...", "task":"team-lookup" }
POST /resume     { "session_id":"..." }
GET  /health
```

## Run

Two processes — backend then agent:

```bash
# terminal 1: backend
cd yard/examples/rfnry/backend
uv sync --extra dev
uv run poe dev          # http://127.0.0.1:8200

# terminal 2: agent
cd yard/examples/rfnry/marketplace-assistant/server-client-python
cp .env.example .env
uv sync --extra dev
uv run poe dev          # http://127.0.0.1:8103
```

## Drive a turn

```bash
curl -X POST http://localhost:8103/turn \
  -H 'content-type: application/json' \
  -d '{
    "session_id": "sales-mike-1",
    "task": "team-lookup",
    "message": "What is the current stock + price for ELEC-RTR-7800? Any active promotions on networking gear?"
  }'
```

The agent should hit `Stock(sku=ELEC-RTR-7800)`, `Catalog(sku=ELEC-RTR-7800)`,
and `Promotions()` — then return the facts plain.
