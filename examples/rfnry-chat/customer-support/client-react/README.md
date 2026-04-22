# customer-support — react frontend

Single-screen chat that connects a fresh **guest user per tab** to the customer-support backend.

- Each tab mints a new `UserIdentity` (random UUID + `Guest-####` name) on load.
- The moment the client connects, the app creates a brand-new thread and invites the agent.
- Opening the app in multiple tabs yields multiple guests, each with their own thread.

## Layout

```
src/
  main.tsx       root + StrictMode
  app.tsx        guest identity + ChatProvider
  chat.tsx      fresh thread + message input
  ui.tsx         <EventFeed>, input/button classes
  styles.css     tailwind entry
```

## Run

```bash
# Start the backend first (see ../server-client-python/README.md).

cd yard/examples/rfnry-chat/customer-support/client-react
cp .env.example .env    # optional — only VITE_CHAT_SERVER_URL override lives here
npm install
npm run dev             # http://localhost:5173
```

The React client auto-encodes the guest identity into the `x-rfnry-identity` header — no auth plumbing.

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
