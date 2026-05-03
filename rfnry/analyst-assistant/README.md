# analyst-assistant — rfnry agent example

A market-research assistant for a small consultancy. Each `client_id`
is a separate engagement; the firm bills clients monthly and runs the
weekly summary every Monday morning. The example exists to demonstrate
**rfnry's native observability + telemetry** — the per-client cost
and latency numbers are the literal billing line, not decoration.

## What this example demonstrates

| rfnry feature | What you see |
|---|---|
| **Markdown agent tree** | `agent/{AGENT.md,INDEX.md,rules,skills,tools,tasks}` — one folder per concept; every file is plain markdown editable on GitHub. |
| **Multi-tenant scope** | `namespaces=["client_id"]`. State partitions under `data/<client_id>/`; the path-jail blocks cross-client reads. |
| **`output_schema`** | Each task declares a Pydantic model (`MarketScan`, `CompetitorProfile`, `WeeklySummary`); the engine validates the model's reply via Pydantic before returning. |
| **Native observability** | The engine emits structured JSONL log records to stderr at every meaningful boundary (turn start/complete, tool call/result, refining/critic errors). Always on; swap the sink to ship logs to ELK/Loki/Datadog. |
| **Native telemetry** | One `TelemetryRow` per turn lands in `data/<client_id>/state.db.telemetry` — tokens (input/output/cache_creation/cache_read), durations, counts, model identity. Always on; the admin UI queries the SQLite directly. |
| **Per-client cost rollup** | `GET /telemetry/{client_id}` aggregates the SQLite rows. The admin UI applies its own rate card to the token totals (the engine ships zero pricing knowledge). |
| **Refining loop** | `RefiningTasksConfig(lookback=10)` opts into per-turn reflections + critic outcomes per client. `POST /consolidate` distills accumulated reflections into eval-gated lessons that load into the next boot bundle for that client only. |

## Layout

```
analyst-assistant/
├── server-client-python/   the rfnry Agent + FastAPI server  (port 8103)
├── data-backend/           mock market-data API              (port 8204)
└── docker-compose.yml      brings up both services
```

## Run with Docker Compose

```bash
docker compose up -d
docker compose logs -f
```

## Run native

```bash
# terminal 1
cd data-backend && uv sync --extra dev && uv run poe dev      # 8204

# terminal 2
cd server-client-python && cp .env.example .env && uv sync --extra dev && uv run poe dev   # 8103
```

## Endpoints

```
agent          POST /turn         { "session_id":"...", "client_id":"...", "message":"...", "task":"market-scan" }
               POST /resume       { "session_id":"...", "client_id":"..." }
               POST /consolidate  { "client_id":"...", "task":"market-scan" }
               GET  /telemetry/{client_id}    aggregated tokens + durations from state.db
               GET  /health
data-backend   GET /companies, /companies/{ticker}, /market-snapshot/{ticker}, /news/{ticker}
```

## Try it

```bash
curl -X POST http://localhost:8103/turn -H 'content-type: application/json' \
  -d '{"session_id":"s1","client_id":"acme","message":"give me a quick scan on QXLR","task":"market-scan"}'
```

After a few turns:

```bash
curl http://localhost:8103/telemetry/acme | jq .totals
# { "turns": 4, "input": 6201, "output": 1408, "cache_read": 12000, ... }
```

That `{tokens × rate-card}` is what your admin UI does. The engine
gives you the numbers; pricing lives where the slicing happens.

## Why per-client telemetry matters here

A research firm bills clients monthly. The signals you need:

- **Per-client token totals** — the billing line.
- **Per-task latency p99** — `weekly-summary` runs Monday morning and
  has an SLA; if p99 climbs, you investigate before the client notices.
- **`reflection_emitted` / `outcome_quality`** — refining health per
  engagement. A client whose turns score consistently low is one where
  your task definition isn't matching the actual question.

All of these queries are `SELECT scope_leaf, … FROM telemetry GROUP BY …`
on the per-client `state.db`. The admin UI repo owns the dashboards;
rfnry owns the rows.
