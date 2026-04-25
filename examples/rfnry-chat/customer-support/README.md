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
