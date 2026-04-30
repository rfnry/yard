# marketplace-assistant — rfnry agent example

An internal assistant for the Sales and Marketing teams at an
electronics retailer. The team relies on it to know "what is the
current state of our catalog, stock, orders, shipping, payments,
promotions, and recent sales" — straightforward lookups, not
analysis or recommendations.

The assistant calls the mock backend on port `8200` for all data.

## Run with Docker Compose

```bash
docker compose up -d
docker compose logs -f
```

Service: `agent` (port `8103`). Requires `backend` (port `8200`).

## Endpoints

```
POST /turn       { "session_id":"...", "message":"...", "task":"team-lookup" }
POST /resume     { "session_id":"..." }
GET  /health
```
