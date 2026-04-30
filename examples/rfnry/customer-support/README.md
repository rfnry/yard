# customer-support — rfnry agent example

Standalone HTTP server that wraps a single rfnry `Agent` configured for a
customer-support task. Per-turn reflection on, eval gate ready, lessons
write to the local `data/` tree.

The agent is the directory at `server-client-python/agent/`. The model
navigates that tree with the built-in `Read`/`Grep`/`Glob`/`LS` tools.

See `server-client-python/README.md` for run instructions.

## Run with Docker Compose

```bash
docker compose up -d
docker compose logs -f agent
```

Service: `agent` (port `8101`).

## Endpoints

```
POST /turn       { "session_id": "...", "message": "...", "task": "resolve-customer-issues" }
POST /resume     { "session_id": "..." }
GET  /health
```
