# support-assistant — client-react

Read-only dashboard for the support-assistant. Two columns: active call queue (left), per-call event log (right). All data via SSE from the FastAPI server.

```bash
npm install
cp .env.example .env  # set VITE_API_URL
npm run dev           # listens on :5173
```
