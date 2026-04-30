# support-assistant — rfnry agent example

A car-parts factory's internal support assistant. The Customer Support
team forwards a customer issue with their own framing notes; the
assistant resolves it by looking up real data — catalog, orders,
shipping, payments, customer profile — through HTTP tools that hit
the mock backend on port `8200`.

This is **not** a marketplace agent for end customers. It's an
internal tool: a CS rep sends a structured message, the assistant
returns a plan of action.

Knowledge: warranty + return + replacement policies live under
`agent/knowledge/`.

## Run with Docker Compose

```bash
docker compose up -d
docker compose logs -f
```

Service: `agent` (port `8101`). Requires `backend` (port `8200`) to
be running — start it from `yard/examples/rfnry/backend/`.

## Endpoints

```
POST /turn       { "session_id":"...", "message":"...", "task":"resolve-customer-issue" }
POST /resume     { "session_id":"..." }
GET  /health
```
