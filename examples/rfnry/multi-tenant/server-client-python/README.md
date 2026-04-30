# multi-tenant — server

Demonstrates rfnry's scope isolation. The agent declares
`namespaces=["org_id", "user_id"]`; every request must supply both.
rfnry validates them into a path-leaf and the path-jail blocks all
cross-tenant access by construction.

## Endpoints

```
POST /turn       { "session_id":"...", "org_id":"...", "user_id":"...", "message":"..." }
POST /resume     { "session_id":"...", "org_id":"...", "user_id":"..." }
GET  /health
```

## Run

```bash
cd yard/examples/rfnry/multi-tenant/server-client-python
cp .env.example .env
uv sync --extra dev
uv run poe dev      # serves on $PORT (default 8102)
```

## Demo two tenants

```bash
# acme/alice
curl -X POST http://localhost:8102/turn \
  -H 'content-type: application/json' \
  -d '{
    "session_id": "alice-1",
    "org_id": "acme",
    "user_id": "alice",
    "message": "Hi, what can you do?"
  }'

# acme/bob
curl -X POST http://localhost:8102/turn \
  -H 'content-type: application/json' \
  -d '{
    "session_id": "bob-1",
    "org_id": "acme",
    "user_id": "bob",
    "message": "Hi, what can you do?"
  }'
```

State partitions on disk:

```
data/acme/alice/sessions/alice-1/events.jsonl
data/acme/bob/sessions/bob-1/events.jsonl
data/acme/alice/state.db    # alice's lessons
data/acme/bob/state.db      # bob's lessons
```

Path-jail enforces the partition: even if the model tries to
`Read("../bob/state.db")` mid-turn, the call is rejected before it
reaches the filesystem.

## Inspect

```bash
uv run rfnry inspect sessions ./agent --scope org_id=acme,user_id=alice
uv run rfnry inspect lessons ./agent --scope org_id=acme,user_id=alice --task support
```
