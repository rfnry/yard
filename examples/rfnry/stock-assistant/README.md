# stock-assistant — rfnry agent example

Standalone HTTP server that wraps a single rfnry `Agent` with one
declarative HTTP tool (`Quote`) wired to a stub stock-quote endpoint
hosted in the same FastAPI process. Demonstrates rfnry's
**zero-Python HTTP tool** primitive: the tool is one TOOL.md file
under the agent tree, no tool-side Python required.

See `server-client-python/README.md` for run instructions.

## Run with Docker Compose

```bash
docker compose up -d
docker compose logs -f agent
```

Service: `agent` (port `8103`).

## Endpoints

```
POST /turn       { "session_id":"...", "message":"...", "task":"quote-lookup" }
POST /resume     { "session_id":"..." }
GET  /quote/{ticker}    stub upstream the agent's HTTP tool calls
GET  /health
```
