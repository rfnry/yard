# team-communication

Slack-shaped reference example for `rfnry-chat`. Demonstrates:

- **Channels** via tenant rooms (`multi-tenant`-style visibility).
- **DMs** via membership (`stock-assistant`-style access), with stable thread ids derived from the participant pair's sorted `client_id`.
- **Live presence** — "who's online" broadcast over Socket.IO via the library's `presence:joined` / `presence:left` frames, hydrated on load via `GET /chat/presence`.
- **Proactive ping control** — each agent exposes two webhooks (`/ping-channel`, `/ping-direct`) that cause the agent to stream a persona-appropriate message into the target thread using Anthropic. The "subject" is picked from a mock pool; the prose is LLM-generated in real time.

The hybrid `authorize` callback (channels public, DMs member-only) is the defining twist: both access patterns coexist in one example server.

## Layout

```
team-communication/
├── server-python/         standalone chat server (in-memory, hybrid authorize + DM filter override)
├── client-python-a/       Agent A — Engineering Manager persona (port 9100)
├── client-python-b/       Agent B — Release Coordinator persona (port 9101)
├── client-python-c/       Agent C — Support Liaison persona (port 9102)
└── client-react/          frontend (port 5173)
```

See each subfolder's `README.md` for subsystem-specific run instructions.

## The model

**Channels** declare `tenant = {channel: "<slug>"}`; users and agents both carry `tenant.channel = "*"` (wildcard), so they naturally discover every channel thread via `list_threads`. Access: `authorize` returns `True` for any thread with `metadata.kind == "channel"`.

**DMs** declare `tenant = {}` (trivially matches every caller) with `metadata.kind == "dm"`. The server example also wraps `GET /chat/threads` to drop DM threads the caller isn't a member of — without that example-level filter, `list_threads` would return every DM to every user (matching semantics, but leaking DM existence). Access: `authorize` falls back to `store.is_member`.

**Presence** is a library primitive: every authenticated socket auto-joins a `presence:<tenant_path>` room; the server broadcasts `presence:joined` / `presence:left` frames on the 0→1 and 1→0 socket-count edges per identity (multi-tab and reconnect blips are silent). Clients hydrate once via `GET /chat/presence`, then patch live.

**The ping control** is decoupled from the open thread: pick any online agent and any channel, fire a webhook, agent streams an opener in character.

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

Service names: `server`, `agent-a`, `agent-b`, `agent-c`, `web`

Place agent-side `.env` files in each agent's source dir (e.g.
`client-python-a/.env`). The compose file loads them via `env_file:`
with `required: false` so the file is optional.

## Running

Five terminals:

```bash
# 1. chat server
cd server-python       && uv sync --extra dev && uv run poe dev

# 2-4. agents
cd client-python-a     && uv sync --extra dev && uv run poe dev
cd client-python-b     && uv sync --extra dev && uv run poe dev
cd client-python-c     && uv sync --extra dev && uv run poe dev

# 5. frontend
cd client-react        && npm install          && npm run dev
# http://localhost:5173
```

Optional: `export ANTHROPIC_API_KEY=sk-ant-...` for real streamed replies. Without it, agents fall back to a one-shot `[stub Agent X] subject: <topic>` message so routing still demos end-to-end.

Open multiple browser tabs to simulate different users.

## Mentions and routing

Channels in this example use **server-side mention routing**:

- Type `@<handle>` anywhere in your message to address a specific teammate. Available handles in the seeded channels: `engineer`, `coordinator`, `liaison` (the three agents). User handles use their identity ids.
- The composer has a Slack-like `@`-trigger picker: typing `@` opens a member list, filter by typing, pick with Enter or click. Selection inserts the literal `@<id> ` (id + space) into the textarea — that's also exactly what hits the wire.
- The server parses the message text, finds every `@<handle>` token, and sets `recipients` on the broadcast event. Multiple handles in one message produce a single event with multiple recipients.
- Messages with no `@<handle>` have `recipients = None` (broadcast). Agents in channels DON'T respond to broadcast messages — they only react when explicitly mentioned. Channels are watch-only until pinged.

**The `@` is a typing convention, not a separate event.** You see your typed text in the feed exactly as written; the React UI styles known `@<id>` tokens as chips with the member's display name. Other channel members SEE every message regardless of recipients (per the "recipients are semantic, not delivery" rule in CLAUDE.md) — but only mentioned recipients' handlers fire.

DMs are unaffected — implicit single-recipient routing applies.

## Verification checklist

1. Start server + three agents + frontend (five terminals).
2. Open two browser tabs → each shows the other in the sidebar **Users** section; both show all three online agents under **Assistants**.
3. Close one of the tabs → the other tab's Users list updates within a socket-disconnect latency (~1s).
4. Click `#general` in tab A, send "hi" → tab B sees the message appear in its `#general` view.
5. Click the other user's name in tab A → DM thread opens; the new DM thread is not visible in any OTHER user's sidebar (only its two participants see it).
6. In the TopControl, pick Agent B + `#general` → click "Ping in channel" → `#general` shows a streamed `@Alice ...` message to every tab in the channel (with `ANTHROPIC_API_KEY` set, typing is visible; otherwise the stub message appears).
7. In the TopControl, pick Agent C → click "Ping me direct" → a DM with Agent C auto-opens in your tab only; the message streams in.

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

One row per `Run` is written to per-tenant SQLite. Three agents share this host so each
client process gets its own `var/<role>/` subdirectory to avoid collision; the server
writes under its own `server-python/var/`:

- Server: `server-python/var/<scope_leaf>/state.db`
- Agent A: `client-python-a/var/agent-a/<scope_leaf>/state.db`
- Agent B: `client-python-b/var/agent-b/<scope_leaf>/state.db`
- Agent C: `client-python-c/var/agent-c/<scope_leaf>/state.db`

```sh
sqlite3 server-python/var/default/state.db \
  "SELECT scope_leaf, status, COUNT(*) AS runs, AVG(duration_ms) AS avg_ms \
   FROM telemetry GROUP BY scope_leaf, status"
```

The `var/` dirs are gitignored — the runtime DB never gets committed.

## References

- Design doc: [`../../../../chat/docs/plans/2026-04-23-team-communication-design.md`](../../../../chat/docs/plans/2026-04-23-team-communication-design.md)
- Implementation plan: [`../../../../chat/docs/plans/2026-04-23-team-communication-impl.md`](../../../../chat/docs/plans/2026-04-23-team-communication-impl.md)
- Library presence primitive:
  - [`../../../../chat/packages/server-python/src/rfnry_chat_server/server/presence.py`](../../../../chat/packages/server-python/src/rfnry_chat_server/server/presence.py)
  - [`../../../../chat/packages/server-python/src/rfnry_chat_server/broadcast/socketio.py`](../../../../chat/packages/server-python/src/rfnry_chat_server/broadcast/socketio.py)
  - [`../../../../chat/packages/server-python/src/rfnry_chat_server/server/rest/presence.py`](../../../../chat/packages/server-python/src/rfnry_chat_server/server/rest/presence.py)
  - React hook: [`../../../../chat/packages/client-react/src/hooks/useChatPresence.ts`](../../../../chat/packages/client-react/src/hooks/useChatPresence.ts)
