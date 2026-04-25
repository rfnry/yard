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
