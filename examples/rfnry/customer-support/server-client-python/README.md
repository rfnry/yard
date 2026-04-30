# customer-support — server

One FastAPI process. The agent is the markdown tree at `agent/`; the
server wraps a single `rfnry.Agent` instance and exposes three endpoints:

```
POST /turn       run a turn for a session
POST /resume     resume a partial turn after a crash / reload
GET  /health     liveness probe
```

## Layout

```
agent/                        the agent the model navigates
  AGENT.md
  INDEX.md
  instructions/
  skills/
  tasks/resolve-customer-issues/

src/
  main.py        FastAPI app + Agent construction
  routes.py      /turn /resume /health
  provider.py    AnthropicProvider | MockProvider selection
```

## Run

```bash
cd yard/examples/rfnry/customer-support/server-client-python
cp .env.example .env       # ANTHROPIC_API_KEY is optional (mock if unset)
uv sync --extra dev
uv run poe dev             # serves on $PORT (default 8101)
```

Per-scope state lands under `data/<scope_leaf>/`:

```
data/default/
  sessions/<session_id>/events.jsonl    append-only event log
  tasks/resolve-customer-issues/
    reflections/<session_id>/<turn>.md
    outcomes/<session_id>/<turn>.md
    lessons/{pending,approved,rejected}/<lesson_id>.md
  state.db                              sqlite (lessons, reflections,
                                        outcomes, consolidations, eval, edits)
```

## Inspect

```bash
uv run rfnry inspect sessions ./agent --scope namespace=default
uv run rfnry inspect lessons ./agent --scope namespace=default --task resolve-customer-issues
uv run rfnry inspect edits ./agent --scope namespace=default
```

## Drive a turn from the shell

```bash
curl -X POST http://localhost:8101/turn \
  -H 'content-type: application/json' \
  -d '{
    "session_id": "demo-1",
    "message": "Customer says their package arrived damaged. What do I do?",
    "task": "resolve-customer-issues"
  }'
```
