# stock-assistant — react dashboard

Always-connected dashboard for the stock-assistant. Every tab is a **new user** (random UUID shown in the header). All users share the same thread list.

- Thread list in the sidebar, plus `+ new` to open a fresh thread (the agent is auto-added as a member).
- Click a thread to open its chat and talk to the stock-assistant.
- The **alert widget** above the chat lets you POST to `/alert-user` on the agent's webhook server. You can call the agent on yourself or on another tab's user id — useful for testing the inverted flow:
  - *new thread* mode: the agent opens a brand-new thread for that user.
  - *into existing thread* mode: the agent posts into the selected thread (auto-filled with the current selection).

When a `thread:invited` arrives — i.e. the agent opened a thread for you via `/alert-user` — the dashboard auto-selects that new thread.

## Layout

```
src/
  main.tsx           root + StrictMode
  app.tsx            guest identity + ChatProvider + layout
  sidebar.tsx        thread list + "+ new thread"
  thread-panel.tsx   events + message input
  alert-widget.tsx   POST /alert-user form (user_id + optional thread_id)
  ui.tsx             <EventFeed>, shared classes
```

## Run

```bash
# 1. chat server  →  ../server-python
# 2. agent + /alert-user webhook  →  ../client-python

cd yard/examples/rfnry-chat/stock-assistant/client-react
cp .env.example .env    # optional — VITE_CHAT_SERVER_URL + VITE_AGENT_WEBHOOK_URL overrides
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
