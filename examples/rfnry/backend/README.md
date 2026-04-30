# backend — mock data server for rfnry examples

A single FastAPI server that hosts mocked endpoints for the three
agent examples' HTTP tool calls. Runs on port `8200` independently of
the agent servers; each agent's `TOOL.md` files point here.

## Domains

```
GET /support-assistant/...      car-parts factory CS data (catalog, orders, shipping, payments, customers)
GET /marketplace-assistant/...  electronics retailer sales/marketing data (catalog, stock, orders, shipping, payments, promotions, sales-summary)
GET /legal-assistant/...        litigation lookups (identity, criminal records, court records, property, business, employment)
```

All data is deterministic — derived by hashing the input — so runs
are reproducible without a database. See each domain's `data.py` for
the dataset shape.

## Layout

```
src/
  main.py                         FastAPI bootstrap, mounts the three domain routers
  support_assistant/
    routes.py services.py data.py
  marketplace_assistant/
    routes.py services.py data.py
  legal_assistant/
    routes.py services.py data.py
```

## Run

```bash
cd yard/examples/rfnry/backend
cp .env.example .env
uv sync --extra dev
uv run poe dev          # serves on $PORT (default 8200)
```

## Smoke

```bash
curl http://localhost:8200/health
curl http://localhost:8200/support-assistant/catalog/PART-12345
curl 'http://localhost:8200/marketplace-assistant/catalog/search?q=router'
curl http://localhost:8200/legal-assistant/identity/ID-9876
```

## Compose

```bash
docker compose up -d
```

Service: `backend` (port `8200`). Run alongside the three agent
example compose files; they all bind to the host network on different
ports.
