# analyst-assistant — agent server

The rfnry agent + FastAPI server for the analyst-assistant example.
See the parent `README.md` for what the example demonstrates and how
to run it.

## Layout

```
agent/                     the markdown tree the model navigates
├── AGENT.md               identity + style
├── INDEX.md               navigation map
├── rules/                 cite-source, no-speculation, triage-first
├── skills/                pull-market-snapshot, scan-sector
├── tools/                 list_companies, company_profile, market_snapshot, news
└── tasks/                 market-scan, competitor-profile, weekly-summary
                          (each declares an output_schema)

src/
├── main.py                FastAPI entry point
├── routes.py              /turn /resume /consolidate /telemetry/{client_id}
└── agent/
    ├── server.py          Agent(...) wired with namespaces=["client_id"],
    │                      output_schemas={...},
    │                      RefiningConfig(methods=[RefiningTasksConfig(lookback=10)])
    ├── schemas.py         MarketScan, CompetitorProfile, WeeklySummary
    ├── turn.py            routes by task → agent.turn(..., expect=Cls)
    ├── resume.py
    └── consolidate.py
```

## Per-client state

```
data/acme/
  sessions/<sid>/events.jsonl                lossless event log
  state.db                                   AgentStore + telemetry table
  refining/reflections/<task>/<sid>/<turn>.md
  refining/outcomes/<task>/<sid>/<turn>.md
  refining/lessons/<task>/{pending,approved,rejected}/
data/contoso/
  ...                                        fully isolated mirror
```

The path-jail blocks `data/contoso/...` from being read while the
agent is serving an `acme` request, even if the model emits a tool
call that tries to.

## Refining (per-client)

```bash
curl -X POST http://localhost:8103/turn -H 'content-type: application/json' \
  -d '{"session_id":"a-1","client_id":"acme","message":"...","task":"market-scan"}'
# ... a few more turns ...
curl -X POST http://localhost:8103/consolidate -H 'content-type: application/json' \
  -d '{"client_id":"acme","task":"market-scan"}'
# Patterns from acme's turns are clustered into lessons; they load
# into the next boot bundle for acme. contoso never sees them.
```

## Telemetry (per-client)

Every turn writes one row to `data/<client_id>/state.db.telemetry`.
The `/telemetry/{client_id}` endpoint demonstrates the read pattern
the admin UI uses:

```bash
curl http://localhost:8103/telemetry/acme | jq '.totals'
# {
#   "turns": 12,
#   "input": 18420,
#   "output": 4112,
#   "cache_creation": 1800,
#   "cache_read": 36240,
#   "duration_ms": 24180,
#   "tool_calls": 28,
#   "tool_errors": 1
# }
```

## Observability (always on)

By default the agent emits one JSON line per significant event to
stderr (`turn.start`, `tool.call`, `tool.result`, `tool.error`,
`output_schema.retry`, `refining.error`, `critic.error`,
`turn.complete`). Pipe stderr to a file or a log shipper:

```bash
uv run poe dev 2>>logs/agent.jsonl
```

To swap the sink (file, Datadog, OTEL exporter, …), construct the
agent with a different `Observability(sink=...)`.
