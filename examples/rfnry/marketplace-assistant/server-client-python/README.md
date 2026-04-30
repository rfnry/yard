# marketplace-assistant — server

Two clean layers:

- `src/main.py` — HTTP infrastructure (FastAPI, CORS, uvicorn).
- `src/app.py` — application layer (Agent construction, agent root,
  inline `AnthropicProvider` from `ANTHROPIC_API_KEY`).
- `src/routes.py` — `POST /turn`, `POST /resume`, `GET /health`.

Agent tree at `agent/`:

```
agent/
  AGENT.md INDEX.md
  instructions/
  skills/
  tools/         catalog, stock, orders, shipping, payments, promotions, sales-summary
  tasks/team-lookup.md
```

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
