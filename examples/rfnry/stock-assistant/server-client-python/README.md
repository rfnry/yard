# stock-assistant — server

Single FastAPI process. Two responsibilities:

1. Hosts the agent's stub upstream — `GET /quote/{ticker}` — that
   returns deterministic JSON (`{"ticker":"AAPL","price":189.42}`).
2. Hosts the rfnry `Agent` whose tree includes one declarative HTTP
   tool (`tools/quote/TOOL.md`) pointing at that stub.

The agent therefore has a real HTTP tool with **zero tool-side Python**:
the engine reads `TOOL.md`, builds an input model, and dispatches
through `HttpExecutor`.

## Endpoints

```
POST /turn              run a turn (the model calls /quote internally)
POST /resume            resume a partial turn
GET  /quote/{ticker}    stub upstream — deterministic JSON
GET  /health
```

## Run

```bash
cd yard/examples/rfnry/stock-assistant/server-client-python
cp .env.example .env
uv sync --extra dev
uv run poe dev          # serves on $PORT (default 8103)
```

## Drive a turn

```bash
curl -X POST http://localhost:8103/turn \
  -H 'content-type: application/json' \
  -d '{
    "session_id": "demo-1",
    "message": "What is AAPL trading at?",
    "task": "quote-lookup"
  }'
```

The agent will call `Quote(ticker="AAPL")` against the local stub
upstream and report back. With `ANTHROPIC_API_KEY` unset, the stub
provider does not call any tools — set the key to see the full loop.

## Inspect

```bash
uv run rfnry inspect sessions ./agent --scope namespace=default
uv run rfnry inspect lessons ./agent --scope namespace=default --task quote-lookup
```
