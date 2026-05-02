# customer-support

Reference example for `rfnry-chat`. One process bundles the chat server and an
LLM-backed support agent that answers user messages via Anthropic.

See `server-client-python/README.md` for subsystem-specific run instructions.

## Run with Docker Compose

```bash
# start everything in detached mode
docker compose up -d

# tail logs (all services)
docker compose logs -f

# tail one service
docker compose logs -f <service>

# restart a service after editing source
docker compose restart <service>

# pick up new .env values (compose only re-reads env on recreate)
docker compose up -d --force-recreate <service>

# stop and remove containers
docker compose down
```

Service names: `agent`, `web`

Place the agent `.env` file in the agent's source dir (`server-client-python/.env`).
The compose file loads it via `env_file:` with `required: false` so the file is optional.

## Observability + Telemetry

This example uses the always-on observability + telemetry shipped with `rfnry-chat-server` / `rfnry-chat-client`. Because this example bundles the chat server and the support agent in **one process**, both write into the same `var/` tree — so we split them by role:

- Server: `data_root=Path("./var/server")` → `server-client-python/var/server/<scope_leaf>/state.db`
- Agent : `data_root=Path("./var/agent")`  → `server-client-python/var/agent/<scope_leaf>/state.db`

That keeps server-side run telemetry distinct from the agent's, even though they share the cwd.

### Live tail (stderr)

In a TTY, log records are pretty-printed with colors. From `docker compose logs -f`, default is JSONL (no TTY detected). Force a mode:

```sh
RFNRY_OBSERVABILITY_FORMAT=pretty docker compose up
RFNRY_OBSERVABILITY_FORMAT=json docker compose up | jq .
```

Set `NO_COLOR=1` to disable colors in pretty mode.

### Telemetry SQLite

```sh
sqlite3 server-client-python/var/server/default/state.db \
  "SELECT scope_leaf, status, COUNT(*) AS runs, AVG(duration_ms) AS avg_ms \
   FROM telemetry GROUP BY scope_leaf, status"

sqlite3 server-client-python/var/agent/default/state.db \
  "SELECT scope_leaf, status, COUNT(*) AS runs, AVG(duration_ms) AS avg_ms \
   FROM telemetry GROUP BY scope_leaf, status"
```

The `var/` dir is gitignored — the runtime DB never gets committed.
