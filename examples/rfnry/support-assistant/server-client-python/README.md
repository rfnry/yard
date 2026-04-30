# support-assistant — server

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
  navigates** (AGENT.md, rules/, knowledge/, skills/, tools/,
  tasks/resolve-customer-issue.md). Edit on GitHub; no Python
  required to author.
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
POST /turn       { "session_id":"...", "message":"...", "task":"resolve-customer-issue" }
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
cd yard/examples/rfnry/support-assistant/server-client-python
cp .env.example .env
uv sync --extra dev
uv run poe dev          # http://127.0.0.1:8101
```

## Drive a turn

A CS rep forwards a customer issue:

```bash
curl -X POST http://localhost:8101/turn \
  -H 'content-type: application/json' \
  -d '{
    "session_id": "rep-amy-1",
    "task": "resolve-customer-issue",
    "message": "Customer CUST-7711 says brake caliper PART-12345 they bought (order ORD-100045) arrived warped. They want a replacement; CS supervisor approved expedited shipping. What do we tell them?"
  }'
```

The agent will look up the order, the part, the shipment status, and
the customer profile via tool calls — then produce a plain-text
recommendation grounded in those lookups and the policy knowledge.

## Inspect

```bash
uv run rfnry inspect sessions ./agent --scope namespace=default
uv run rfnry inspect lessons ./agent --scope namespace=default --task resolve-customer-issue
```
