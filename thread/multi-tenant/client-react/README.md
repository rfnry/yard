# multi-tenant — react frontend

Org + workspace + role switcher with a thread list. Tied to the standalone chat server at `http://localhost:8000` and the two org-scoped agents. See [`../README.md`](../README.md) for the full conceptual model and role matrix.

- Every tab mints a fresh `UserIdentity` (random UUID + `Guest-####`). That identity persists while the tab is open.
- The **role selector** (`member` / `workspace-manager` / `org-manager` / `system-admin`) rewrites the identity's tenant wildcards. `tenants.ts#tenantFor()` is the single source of truth for that mapping.
- Pick an organization, a workspace, and a role — the `ChatProvider` remounts via its `key` so `listThreads` refetches filtered to the new tenant shape.
- Creating a thread writes `tenant: { organization, workspace, author: guest.id }`. No `addMember` of the agent: the server's custom `authorize` trusts tenant, and each agent joins tenant-matching threads on its own via `on_connect` + a 10s poll.
- Messages are sent without `recipients` — the room is the audience. The tenant-matching agent picks them up and replies.

## Layout

```
src/
  main.tsx          root + StrictMode
  app.tsx           state (org/workspace/role/selected thread), ChatProvider, layout
  sidebar.tsx       org + workspace + role selectors, thread list, "+ new thread"
  thread-panel.tsx  events + message input for the selected thread
  tenants.ts        org/workspace definitions, agent identities, role → tenant mapping
  ui.tsx            <EventFeed>, shared classes
```

## Run

```bash
# 1. Start the chat server (see ../server-python/README.md):
#    uv run uvicorn src.main:asgi --port 8000

# 2. Start agent-a (see ../client-python-a/README.md):
#    uv run python -m src.main

# 3. Start agent-b (see ../client-python-b/README.md):
#    uv run python -m src.main

# 4. Start the frontend:
cd yard/examples/rfnry-chat/multi-tenant/client-react
cp .env.example .env    # optional — only VITE_CHAT_SERVER_URL override lives here
npm install
npm run dev             # http://localhost:5173
```

## Development

Scripts in `package.json`:

```bash
npm install

npm run dev          # vite dev server
npm run build        # tsc -b && vite build
npm run preview      # vite preview

npm run format       # biome format --write .
npm run check        # biome check .
npm run check:fix    # biome check --fix .
npm run typecheck    # tsc --noEmit
```
