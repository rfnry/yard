# multi-tenant — rfnry agent example

Standalone HTTP server that wraps a single rfnry `Agent` configured with
two namespaces (`org_id`, `user_id`). Each turn requires both in the
request body; rfnry validates them into a path leaf
(`data/<org_id>/<user_id>/...`) and the path-jail blocks any cross-tenant
read or write — even under prompt injection.

This example demonstrates the **scope isolation** pillar end-to-end.

See `server-client-python/README.md` for run instructions.

## Run with Docker Compose

```bash
docker compose up -d
docker compose logs -f agent
```

Service: `agent` (port `8102`).

## Endpoints

```
POST /turn       { "session_id":"...", "org_id":"...", "user_id":"...", "message":"..." }
POST /resume     { "session_id":"...", "org_id":"...", "user_id":"..." }
GET  /health
```
