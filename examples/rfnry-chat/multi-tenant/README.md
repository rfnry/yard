# multi-tenant

Reference implementation of the **workspace-is-the-room** access model built on top of `rfnry-chat`. Demonstrates how a single chat server can host two independent organizations, each with multiple workspaces and the full system/org/workspace/member role matrix — without ever calling `addMember` per thread.

## Layout

```
multi-tenant/
├── server-python/        standalone chat server (no embedded agent)
├── client-python-a/      agent for organization-a (serves both workspaces)
├── client-python-b/      agent for organization-b (serves both workspaces)
└── client-react/         frontend with org + workspace + role selectors
```

See each subfolder's `README.md` for run instructions.

## The tenant shape

Every identity (user or agent) carries a 3-key tenant under `identity.metadata.tenant`:

```
{ organization: "<org-id>" | "*",
  workspace:    "<workspace-id>" | "*",
  author:       "<user-id>" | "*" }
```

Every thread carries the same three keys at concrete values (never `"*"`):

```
{ organization: "organization-a",
  workspace:    "workspace-a-1",
  author:       "u_alice" }
```

Access is decided by `matches(thread.tenant, identity.tenant)`:

> For every key the thread declares, the identity must carry the same value **or** the literal string `"*"` (wildcard).

That's the whole rule. Every REST and Socket.IO handler in the server calls `matches()` first; the result is the discovery gate. Write operations then call `authorize()` (below).

## The role matrix

The UI's role selector rewrites the identity's tenant wildcards. That single swap is what moves a user up or down the matrix.

| Role                 | Identity tenant                                 | What they see                         |
|----------------------|-------------------------------------------------|---------------------------------------|
| **member**           | `{org, workspace, author: guest.id}`            | only own threads in the workspace     |
| **workspace manager**| `{org, workspace, author: "*"}`                 | every author's threads in that workspace |
| **org manager**      | `{org, workspace: "*", author: "*"}`            | every thread across every workspace in the org |
| **system admin**     | `{organization: "*", workspace: "*", author: "*"}` | every thread in every org           |

Mapping is centralized in `client-react/src/tenants.ts` (`tenantFor(role, orgId, workspaceId, authorId)`). That's the only place the UI layer knows what "manager" means; everything downstream just sees wildcards on a tenant shape.

### Live visibility (verified against a running server)

With four threads in play:

- `th_alice` — `{org-a, ws-a-1, u_alice}`
- `th_bob` — `{org-a, ws-a-1, u_bob}`
- `th_carol` — `{org-a, ws-a-2, u_carol}`
- `th_dave` — `{org-b, ws-b-1, u_dave}`

…each caller's `GET /chat/threads` returns exactly:

| Caller                      | Identity tenant                 | Threads returned                     |
|-----------------------------|---------------------------------|--------------------------------------|
| Alice (member, ws-a-1)      | `{org-a, ws-a-1, u_alice}`      | `th_alice`                           |
| Bob (member, ws-a-1)        | `{org-a, ws-a-1, u_bob}`        | `th_bob`                             |
| Carol (member, ws-a-2)      | `{org-a, ws-a-2, u_carol}`      | `th_carol`                           |
| Frank (ws-mgr, ws-a-1)      | `{org-a, ws-a-1, *}`            | `th_alice`, `th_bob`                 |
| Grace (org-mgr, org-a)      | `{org-a, *, *}`                 | `th_alice`, `th_bob`, `th_carol`     |
| Dave (member, ws-b-1)       | `{org-b, ws-b-1, u_dave}`       | `th_dave`                            |
| Root (system admin)         | `{*, *, *}`                     | all four                             |

Org isolation holds (Grace can't see Dave's org-b thread). Workspace isolation holds (Frank can't see Carol's ws-a-2 thread). Author isolation holds (Alice can't see Bob's thread even though they share a workspace).

## The `authorize` callback

`matches()` decides visibility. **`authorize()` decides everything else** — join, send, cancel run, update thread, delete thread, add/remove member. By default (`authorize=None`) the server falls back to "the caller must be a member of the thread":

```python
# chat/packages/server-python — default
async def check_authorize(identity, thread_id, action, target_id=None):
    if self.authorize is None:
        return await self.store.is_member(thread_id, identity.id)
    return await self.authorize(identity, thread_id, action, target_id=target_id)
```

This example replaces that with **"tenant match is enough"**:

```python
# multi-tenant/server-python/src/chat.py
async def _tenant_is_enough(identity, thread_id, action, *, target_id=None):
    # matches(thread.tenant, identity.tenant) was already checked before
    # authorize fires. If we're here, the identity's tenant shape is
    # compatible with the thread's. In a workspace-is-the-room product,
    # that IS the full access decision.
    return True

server = ChatServer(store=store, authorize=_tenant_is_enough)
```

### Why this matters

With the default membership-as-access model, letting a workspace manager observe every author's thread would require calling `addMember(manager, thread)` on every thread in the workspace, forever. That's coordination at thread-creation time — not scalable, not clean.

With `authorize=_tenant_is_enough`:

- A manager's identity carries `author: "*"`.
- `matches()` lets them discover every author's thread in their workspace via `GET /chat/threads`.
- `authorize()` lets them join any of those threads, send messages, read events.
- **No `addMember` calls anywhere.** The role change is a tenant rewrite, not a DB write.

Other patterns the same shape supports (one authorize function, 3-6 lines of Python each):

- **Mixed-mode** — public workspace threads + opt-in private threads marked `metadata.private=true`. Public ones: `return True`. Private ones: fall back to `store.is_member`.
- **Read-only escalation** — managers can read/join any thread but only write their own. Inspect `action`: for `thread.read` return True unconditionally; for `message.send` fall back to membership.
- **Audit observers** — a dedicated read-only identity with tenant `{*, *, *}` but `authorize` gates anything except `thread.read`.

All of these compose with the same core.

## Agents, without membership

Each organization runs one agent process (`client-python-a`, `client-python-b`). Their identities are tenant-wildcarded at org scope:

```python
AssistantIdentity(
    id="agent-a",
    name="Agent A",
    metadata={"tenant": {
        "organization": "organization-a",
        "workspace":    "*",
        "author":       "*",
    }},
)
```

The agent is **never** added as a thread member. Instead, `main.py` runs a connect hook + periodic poller that:

1. On `ChatClient.run(on_connect=...)` — lists every tenant-visible thread and joins the socket room for each.
2. Every 10 seconds — re-lists threads, joins any new ones.

```python
async def _discover_and_join(client, joined):
    page = await client.rest.list_threads()
    for thread in page["items"]:
        if thread.id in joined: continue
        await client.join_thread(thread.id)
        joined.add(thread.id)
```

`list_threads` is tenant-filtered by the server, so agent-a naturally discovers every org-a thread across both workspaces and nothing from org-b. Agent-b is the mirror.

### Trade-off: polling vs. inbox

Polling has a worst-case discovery latency of `POLL_SECONDS` (10s here). For real-time discovery, an alternative is broadcasting a `thread:created` frame to tenant-matching inboxes on thread creation — that's a larger protocol change and isn't in this example. Polling is a lighter-touch pattern that keeps the chat core unchanged.

## Messaging in workspace-is-the-room

User messages from the frontend omit the `recipients` field entirely:

```ts
send({
  clientId: crypto.randomUUID(),
  content: [{ type: 'text', text }],
  // no `recipients: [agentId]` — the room is the audience
})
```

In this model, "the room" is the thread, and everyone joined to it (via tenant match) sees the event. The agent is joined; its handler fires; it replies. No per-recipient routing is needed.

`recipients` is still useful in examples like `customer-support` where membership IS the access model and filtering a message to a specific agent is meaningful. Both patterns coexist in the same core.

## Identity / authorize matrix — quick reference

```
                 thread.tenant      identity.tenant           matches?   authorize?
member / own     {org, ws, user}    {org, ws, user}           yes        true (tenant)
member / other   {org, ws, user_x}  {org, ws, user_y}         no         —
ws-mgr / own     {org, ws, user}    {org, ws, *}              yes        true
ws-mgr / other   {org, ws, user}    {org, ws, *}              yes        true   ← escalation
ws-mgr / other-ws {org, ws_x, *}    {org, ws_y, *}            no         —
org-mgr          {org, ws_y, user}  {org, *, *}               yes        true   ← escalation
org-mgr / cross-org {org_x, *, *}   {org_y, *, *}             no         —
admin            *any*              {*, *, *}                 yes        true   ← escalation
```

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

Service names: `server`, `agent-a`, `agent-b`, `web`

Place agent-side `.env` files in each agent's source dir (e.g.
`client-python-a/.env`). The compose file loads them via `env_file:`
with `required: false` so the file is optional.

## Running

Four terminals:

```bash
# 1. chat server
cd server-python       && uv sync --extra dev && uv run poe dev

# 2. agent for org-a
cd client-python-a     && uv sync --extra dev && uv run poe dev

# 3. agent for org-b
cd client-python-b     && uv sync --extra dev && uv run poe dev

# 4. frontend
cd client-react        && npm install          && npm run dev
# http://localhost:5173
```

Optional: `export ANTHROPIC_API_KEY=sk-ant-...` for real replies. Without it the agents stub out with a visible `[stub reply from …]` message so you can still see routing end-to-end.

Open multiple browser tabs to simulate different guests. Flip between roles to escalate/de-escalate a given tab without reloading.

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

One row per `Run` is written to per-tenant SQLite. Two agents share this host so each
client process gets its own `var/<role>/` subdirectory to avoid collision; the server
writes under its own `server-python/var/`. With multi-tenant rooted threads, the
`scope_leaf` is the tenant path (e.g. `organization-a__workspace-a-1`):

- Server: `server-python/var/<scope_leaf>/state.db`
- Agent A: `client-python-a/var/agent-a/<scope_leaf>/state.db`
- Agent B: `client-python-b/var/agent-b/<scope_leaf>/state.db`

```sh
sqlite3 server-python/var/default/state.db \
  "SELECT scope_leaf, status, COUNT(*) AS runs, AVG(duration_ms) AS avg_ms \
   FROM telemetry GROUP BY scope_leaf, status"
```

The `var/` dirs are gitignored — the runtime DB never gets committed.
