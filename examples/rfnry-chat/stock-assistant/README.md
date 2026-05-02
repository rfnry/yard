# stock-assistant

Reference example for `rfnry-chat`. Demonstrates a standalone chat server with
an external stock-price agent that responds to queries and can alert users via a
webhook.

See each subfolder's `README.md` for subsystem-specific run instructions.

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

Service names: `server`, `agent`, `web`

Place the agent `.env` file in the agent's source dir (`client-python/.env`).
The compose file loads it via `env_file:` with `required: false` so the file is optional.

## Observability + Telemetry

This example uses the always-on observability + telemetry shipped with `rfnry-chat-server` / `rfnry-chat-client`.

### Live tail (stderr)

In a TTY, log records are pretty-printed with colors. From `docker compose logs -f`, default is JSONL (no TTY detected). Force a mode:

```sh
RFNRY_OBSERVABILITY_FORMAT=pretty docker compose up
RFNRY_OBSERVABILITY_FORMAT=json docker compose up | jq .
```

Set `NO_COLOR=1` to disable colors in pretty mode.

### Telemetry SQLite

One row per `Run` is written to per-tenant SQLite under each process's `var/`:

- Server: `server-python/var/<scope_leaf>/state.db`
- Agent: `client-python/var/<scope_leaf>/state.db`

The two are separate processes with separate working dirs, so they never collide.

```sh
sqlite3 server-python/var/default/state.db \
  "SELECT scope_leaf, status, COUNT(*) AS runs, AVG(duration_ms) AS avg_ms \
   FROM telemetry GROUP BY scope_leaf, status"
```

The `var/` dirs are gitignored — the runtime DB never gets committed.
