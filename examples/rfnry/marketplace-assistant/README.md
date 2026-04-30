# marketplace-assistant — rfnry agent example

An internal assistant for the Sales and Marketing teams at an
electronics retailer. The team relies on it to know "what is the
current state of our catalog, stock, orders, shipping, payments,
promotions, and recent sales" — straightforward lookups, not
analysis or recommendations.

## Layout

```
marketplace-assistant/
├── server-client-python/   the rfnry Agent + FastAPI server    (port 8103)
├── data-backend/           mock data the agent's tools call     (port 8202)
└── docker-compose.yml      brings up both services
```

## Run with Docker Compose

```bash
docker compose up -d
docker compose logs -f
```

## Run native (no docker)

Two terminals:

```bash
# terminal 1
cd data-backend && uv sync --extra dev && uv run poe dev      # 8202

# terminal 2
cd server-client-python && cp .env.example .env && uv sync --extra dev && uv run poe dev   # 8103
```

## Endpoints

```
agent          POST /turn       { "session_id":"...", "message":"...", "task":"team-lookup" }
               POST /resume     { "session_id":"..." }
               GET  /health
data-backend   GET /catalog/{sku}, /stock/{sku}, /sales-summary?period=…   (see data-backend/README.md)
```
