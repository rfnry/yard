# rfnry examples

Two agents across three maturity tiers, showing how an rfnry agent grows from plain Q&A into a self-evolving system.

```
examples/python/
├── server.py                FastAPI — drives every agent via /agents/<path>
├── pyproject.toml           rfnry (editable) + fastapi + uvicorn
├── agents/
│   ├── stock-agent/
│   │   ├── minimal/         plain Q&A, no reflection
│   │   ├── task-reasoning/  + tasks/ + reflection level 2 (critic on)
│   │   └── self-evolving/   + level 3 + org_id scope + consolidate()
│   └── customer-support/
│       ├── minimal/
│       ├── task-reasoning/
│       └── self-evolving/
└── samples/                 real artifacts from a live Anthropic run
    └── customer-support-self-evolving/
        ├── reflections/     3 pre-turn reflections (with engine-injected pattern_hash)
        ├── outcomes/        3 critic evaluations
        ├── learned/         3 synthesized instruction snippets + _index.md
        └── consolidations/  audit trail + consolidations.jsonl
```

Each tier is a complete agent folder — copied, not shared — so `diff -r agents/stock-agent/minimal agents/stock-agent/task-reasoning` shows exactly what grew between tiers.

`samples/` contains committed snapshots of what the system produces when it runs for real. **Look there** if you want to see what reflections, outcomes, and promoted learnings look like without running the example yourself. See [`samples/README.md`](samples/README.md) for what to notice.

## Quick start

```bash
cd examples/python
uv sync
uv run uvicorn server:app --reload
```

Server defaults to `PROVIDER=mock` (no API key, deterministic replies). For real providers:

```bash
PROVIDER=anthropic ANTHROPIC_API_KEY=... uv run uvicorn server:app --reload
PROVIDER=openai    OPENAI_API_KEY=...    uv run uvicorn server:app --reload
```

Default models (override with `MODEL=...`):
- anthropic → `claude-sonnet-4-6`
- openai    → `gpt-4o-mini`

## Two ways to drive it

### HTTP (curl)

```bash
# minimal — plain Q&A
curl -s localhost:8000/agents/stock-agent/minimal/chat \
  -H 'content-type: application/json' \
  -d '{"session_id":"s1","message":"How many WDG-001 in warehouse A?"}'

# task-reasoning — reflection + critic run per turn
curl -s localhost:8000/agents/stock-agent/task-reasoning/chat \
  -H 'content-type: application/json' \
  -d '{"session_id":"s1","message":"How many WDG-001?","task":"stock-check"}'

# self-evolving — multi-tenant + consolidation
curl -s localhost:8000/agents/stock-agent/self-evolving/chat \
  -H 'content-type: application/json' \
  -d '{"session_id":"s1","message":"WDG-002?","scope":{"org_id":"acme"},"task":"stock-check"}'

# after a few turns, consolidate into learned/
curl -s localhost:8000/agents/stock-agent/self-evolving/consolidate \
  -H 'content-type: application/json' \
  -d '{"task":"stock-check","scope":{"org_id":"acme"}}'

# inspect the session's event stream
curl -s 'localhost:8000/agents/stock-agent/self-evolving/events?session_id=s1&scope_leaf=acme'
```

Swap `stock-agent` for `customer-support` to drive the other agent. Same endpoints, same shape.

### CLI

The same folders work with the `rfnry` CLI — no server needed.

```bash
# minimal
rfnry chat agents/stock-agent/minimal \
  --session s1 --provider mock \
  "How many WDG-001 in warehouse A?"

# task-reasoning
rfnry chat agents/stock-agent/task-reasoning \
  --session s1 --task stock-check --provider mock \
  "How many WDG-001?"

# self-evolving — scope required
rfnry chat agents/stock-agent/self-evolving \
  --session s1 --task stock-check \
  --namespace org_id --scope org_id=acme \
  --provider mock "WDG-002?"

# consolidate after N turns
rfnry consolidate agents/stock-agent/self-evolving \
  --task stock-check --namespace org_id --scope org_id=acme \
  --provider mock

# boot bundle with task context — <<<LEARNED>>> appears after consolidate
rfnry boot agents/stock-agent/self-evolving \
  --task stock-check --namespace org_id --scope org_id=acme
```

Swap `--provider mock` for `anthropic` / `openai` to drive real models (with the env vars set).

## What changes between tiers

```bash
diff -r agents/stock-agent/minimal agents/stock-agent/task-reasoning
# → Only in .../task-reasoning/: tasks

diff -r agents/stock-agent/task-reasoning agents/stock-agent/self-evolving
# → TASK.md differs in reflection.level (2 vs 3)
```

The entire self-improvement layer is a single folder addition. Configuration in `TASK.md` is what activates reflection / critic / consolidation. The agent's core identity (AGENT.md, INDEX.md, instructions/, knowledge/) stays identical across tiers.

## Observing the loop

After a few turns at `task-reasoning` or `self-evolving`, the `data/` tree fills up with engine-written artifacts:

```
agents/stock-agent/task-reasoning/data/_default/tasks/stock-check/
├── reflections/s1/1.md   pre-turn reflection, engine-injected pattern_hash
├── reflections/s1/2.md
├── outcomes/s1/1.md      critic verdict + quality_score
└── outcomes/s1/2.md
```

After `consolidate()` at self-evolving:

```
agents/stock-agent/self-evolving/data/acme/tasks/stock-check/
├── learned/<ts>-<hash>.md         promoted instruction snippet
├── learned/_index.md              auto-loaded into next boot bundle
├── consolidations/<ts>.md         audit trail
└── consolidations/consolidations.jsonl
```

Runtime `data/` dirs are gitignored — every run produces fresh artifacts. For committed, browsable examples of what this output actually looks like, see [`samples/`](samples/).

## Running the test suite

Standard unit + integration tests, fast and offline:

```bash
cd packages/python && uv run pytest
```

E2E tests that actually call a real provider are opt-in. Selecting a provider marker means *"use that provider for real"* — it costs tokens and needs credentials:

```bash
# real Anthropic calls — needs ANTHROPIC_API_KEY
pytest -m anthropic

# real OpenAI calls — needs OPENAI_API_KEY
pytest -m openai
```

Without the env var, `pytest -m anthropic` cleanly skips. Bare `pytest` deselects both.

## Provider notes

- **mock** — deterministic, structurally-valid reflections/outcomes. Good for end-to-end pipeline checks without burning tokens. Content is not useful for anything real. Lives at `src/rfnry/providers/mock.py`.
- **anthropic** — cache-aware system split. Boot bundle passes as a cached content block; per-turn reflection becomes a second system block without `cache_control`. First-class adapter at `src/rfnry/providers/anthropic.py`. Install: `uv sync --extra anthropic`.
- **openai** — system-role passthrough. First-class adapter at `src/rfnry/providers/openai.py`. Install: `uv sync --extra openai`.
