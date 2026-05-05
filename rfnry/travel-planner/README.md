# Travel-Planner

A multi-agent **workflow** that plans a trip: four specialist scouts run **in parallel**, and a synthesizer composes their outputs into a single bookable plan.

This example exists to show off two specific rfnry features:

1. **`parallel:` workflow steps** — fan-out / fan-in over independent agents.
2. **Per-step `task:` framing + workflow-level `output_schemas`** — schema-validated reports at every layer.

There are **no teams** here. Each scout is its own agent, registered alongside the others under `agents/`, and the workflow at `agents/WORKFLOW.md` orchestrates them. Teams are for cases where you want a leader to decide delegation dynamically; workflows are for cases where the routing is deterministic and visible.

## What it does

| rfnry feature | What you see |
|---|---|
| **Workflow with `parallel:` step** | Four scouts (flights, hotels, activities, weather) run concurrently via `asyncio.gather`. Wall-clock latency = slowest scout, not the sum. |
| **Per-step `task:` framing** | Each scout's turn loads its own task frontmatter, its own per-task lessons, its own `output_schemas` entry. |
| **Per-task structured output** | Each scout returns a schema-validated Pydantic report (`FlightOptions`, `HotelOptions`, `ActivityList`, `WeatherForecast`). The model self-corrects on `ValidationError` inside its turn. |
| **Workflow-level structured output** | The workflow output is validated as a `TripPlan` on the way out. `engine.run_workflow(name="plan-trip", expect=TripPlan)` returns a typed instance. |
| **Markdown agent tree** | `agents/<name>/{AGENT.md,INDEX.md,rules,skills,knowledge,tools,tasks}` per scout. No Python required to author or modify any agent's behavior. |
| **Native observability + telemetry** | One JSONL record per turn boundary on stderr; one `TelemetryRow` per scout turn (and a workflow's worth) in `data/<traveler_id>/state.db.telemetry`. |

## The workflow shape

```
                ┌─→ flight-scout    (find-flights)    ─┐
                │                                       │
input ──────────┼─→ hotel-scout     (find-hotels)     ─┼──→ trip-synthesizer ──→ TripPlan
                │                                       │
                ├─→ activity-curator (curate-activities)┤
                │                                       │
                └─→ weather-watcher (forecast)         ─┘
       parallel: (asyncio.gather)                       fan-in via placeholders
```

See `server-client-python/agents/WORKFLOW.md` for the literal YAML.

## Layout

```
travel-planner/
├── README.md
└── server-client-python/
    ├── README.md                       # how to run
    ├── pyproject.toml
    ├── agents/
    │   ├── WORKFLOW.md                 # plan-trip: parallel scouts → synthesizer
    │   ├── flight-scout/
    │   ├── hotel-scout/
    │   ├── activity-curator/
    │   ├── weather-watcher/
    │   └── trip-synthesizer/
    └── src/
        ├── engine.py                   # AgentEngine + OutputSchemas
        ├── schemas.py                  # FlightOptions, HotelOptions, …, TripPlan
        ├── provider.py                 # Anthropic adapter
        ├── routes.py                   # POST /plan-trip
        └── server.py
```

## Why this domain fits `parallel:`

The four scouts have **no cross-dependency** until the synthesis step. Each hits an independent data source. Latency is bound by the slowest API, not the sum. This is the ideal shape for fan-out:

- Sequential: ~5s flights + ~5s hotels + ~5s activities + ~3s weather = ~18s wall-clock.
- Parallel: max(5, 5, 5, 3) = ~5s wall-clock.

A failure in one scout doesn't stop the others — though the parent step fails if any child fails (v1 semantic). The synthesizer can also degrade gracefully on partial inputs if you wire its task body to do so.

## RAG / external API integration

Every scout has a `tools/<thing>-search.md` HTTP tool with a stubbed URL pointing at `127.0.0.1:8303/...`. The comment inside each tool file marks where a real provider would land:

- `flight-search.md` → Amadeus / Skyscanner / Duffel / Kiwi
- `hotel-search.md` → Booking.com / Expedia / RateHawk
- `activity-search.md` → Viator / GetYourGuide / Klook + a city-guides RAG index
- `weather-forecast.md` → Open-Meteo / NOAA / Tomorrow.io

rfnry handles the HTTP execution, retries, redaction, and result-spilling for big payloads — the tool stays a single declarative `.md` file.

## Run

See `server-client-python/README.md`.
