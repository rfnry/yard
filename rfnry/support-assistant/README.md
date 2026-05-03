# support-assistant — rfnry agent example

A car-parts factory's internal support assistant. The Customer Support
team forwards a customer issue with their own framing notes; the
assistant resolves it by looking up real data — catalog, orders,
shipping, payments, customer profile — through HTTP tools that hit
its sibling `data-backend/` server.

This is **not** a marketplace agent for end customers. It's an
internal tool: a CS rep sends a structured message, the assistant
returns a plan of action.

Knowledge: warranty + return + replacement policies live under
`server-client-python/agent/knowledge/`.

## Layout

```
support-assistant/
├── server-client-python/   the rfnry Agent + FastAPI server   (port 8101)
├── data-backend/           mock data the agent's tools call    (port 8201)
└── docker-compose.yml      brings up both services
```

## Run with Docker Compose

```bash
docker compose up -d
docker compose logs -f
```

Both services start in one command. The agent's
`BACKEND_BASE_URL` is set to `http://data-backend:8201` over the
internal compose network.

## Run native (no docker)

Two terminals:

```bash
# terminal 1
cd data-backend && uv sync --extra dev && uv run poe dev      # 8201

# terminal 2
cd server-client-python && cp .env.example .env && uv sync --extra dev && uv run poe dev   # 8101
```

## Endpoints

```
agent          POST /turn       { "session_id":"...", "message":"...", "task":"resolve-customer-issue" }
               POST /resume     { "session_id":"..." }
               GET  /health
data-backend   GET /catalog/{part_id}, /orders/{order_id}, ...   (see data-backend/README.md)
```
