# support-assistant — server

Two clean layers:

- `src/main.py` — HTTP infrastructure. FastAPI app, CORS, uvicorn,
  route registration. No agent code here.
- `src/app.py` — application layer. Builds the `rfnry.Agent`,
  resolves the agent root, picks the provider, exposes a singleton
  the routes consume via `app.state`.
- `src/routes.py` — HTTP handlers calling `state.agent`.
- `src/provider.py` — `AnthropicProvider` selection (stub if no key).

The agent's markdown tree lives at `agent/`:

```
agent/
  AGENT.md INDEX.md
  instructions/      one rule per file
  knowledge/         warranty / replacement / refund policies
  skills/            triggerable procedures (warped-part flow, return flow…)
  tools/             declarative HTTP tools pointing at http://127.0.0.1:8200
  tasks/resolve-customer-issue/
```

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
