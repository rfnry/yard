# team-communication — react frontend

Slack-shaped UI for the `team-communication` demo. Tied to the standalone chat server at `http://localhost:8000` and the three agent processes (A on :9100, B on :9101, C on :9102). See [`../README.md`](../README.md) for the full model, access rules, and the seven-step verification checklist.

- Every tab mints a fresh `UserIdentity` (random UUID + `Guest-####`) that persists while the tab is open.
- Sidebar: a `#channel` list (all users see the same channels), a **Users** section (live presence of other humans), an **Assistants** section (live presence of the three agents), and a DM list (only DMs the tab's user is a member of).
- Clicking a user name opens-or-reuses a DM with them (stable per-pair thread id).
- The **TopControl** above the chat lets you fire either webhook on any online agent — "Ping in channel" posts into the currently-selected channel; "Ping me direct" opens a DM with that agent for the current user.

## Layout

```
src/
  main.tsx           root + StrictMode
  app.tsx            guest identity + ChatProvider + layout
  sidebar.tsx        channels + users + assistants + DMs
  thread-panel.tsx   events + message input
  top-control.tsx    agent + channel pickers + ping buttons
  ui.tsx             <EventFeed>, shared classes
```

## Run

```bash
# Prereqs (see ../README.md for the full five-terminal sequence):
#   1. ../server-python      chat server on :8000
#   2. ../client-python-a    Agent A on :9100
#   3. ../client-python-b    Agent B on :9101
#   4. ../client-python-c    Agent C on :9102

cd yard/examples/rfnry-chat/team-communication/client-react
cp .env.example .env    # optional — VITE_CHAT_SERVER_URL + VITE_AGENT_*_WEBHOOK_URL overrides
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
