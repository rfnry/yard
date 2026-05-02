# support-assistant — telephony voice agent (Twilio + OpenAI Realtime)

Demo of `rfnry-voice-server` driving a Twilio inbound phone line through OpenAI's Realtime API. Each call becomes a `VoiceSession`; the React dashboard watches them all over Server-Sent Events.

This example **does not** depend on `rfnry`, `rfnry-chat`, or `@rfnry/voice-client-react`. It exercises only the standalone server SDK + the `[twilio]` and `[openai]` extras.

## Layout

```
support-assistant/
├── server-python/          FastAPI server (port 8301)
│   ├── src/
│   │   ├── main.py         app entry + health
│   │   ├── routes.py       /twilio/voice, /sessions/sse, /sessions/{id}/{kill,clear,events/sse}
│   │   ├── ws.py           /twilio/stream WebSocket endpoint
│   │   ├── manager.py      SessionManager (tracks active calls, SSE fan-out)
│   │   ├── data.py         in-memory rentals + accounts dataset
│   │   ├── tools.py        4 tools: lookup_account, list_rentals, refund_rental, escalate_to_human
│   │   └── agent.py        STS provider + VoiceSession factory
│   └── tests/
└── client-react/           Vite dashboard (port 5173)
    └── src/
        ├── app.tsx         two-column layout
        ├── queue.tsx       left: active call queue with kill/clear buttons
        ├── event-log.tsx   right: read-only event stream of selected call
        └── hooks/          useServerSessions, useSessionEvents (SSE)
```

## Run with Docker Compose

```bash
cp server-python/.env.example server-python/.env  # edit OPENAI_API_KEY + PUBLIC_HOST
docker compose up
# logs:
docker compose logs -f
```

Server: <http://localhost:8301>. Client: <http://localhost:5173>.

## Run native (no docker)

Two terminals:

```bash
# terminal 1 — server
cd server-python && uv sync --extra dev && uv run poe dev    # 8301

# terminal 2 — client
cd client-react && npm install && npm run dev                # 5173
```

## Twilio setup (required for real calls)

1. **Create a Twilio trial account** (<https://www.twilio.com/try-twilio>). You get $15.50 credit and one trial number.
2. **Verify your phone number** so you can call your trial number from it.
3. **Expose your local server** with a tunnel — Twilio needs a public HTTPS URL to webhook into:

```bash
cloudflared tunnel --url http://localhost:8301
# OR
ngrok http 8301
```

Copy the `https://<random>.trycloudflare.com` (or `*.ngrok-free.app`) hostname.

4. **Set `PUBLIC_HOST` in `server-python/.env`** to that hostname (no `https://` prefix).

5. **Configure your Twilio number's voice webhook**:
   - Twilio Console → Phone Numbers → Manage → Active Numbers → click your number.
   - Under *Voice Configuration → A call comes in*, set:
     - Configuration: **Webhook**
     - URL: `https://<PUBLIC_HOST>/twilio/voice`
     - HTTP method: `POST`
   - Save.

6. **Restart the server** so it picks up the new `PUBLIC_HOST`.

7. **Call your Twilio number** from your verified phone. Within ~3 seconds you'll see:
   - Twilio fetches `/twilio/voice` → server returns TwiML pointing at `wss://<host>/twilio/stream`.
   - Twilio opens the Media Stream WS.
   - The dashboard at <http://localhost:5173> shows the new session in the queue.
   - Speak; transcripts and tool calls populate the event log live.

## Test scenarios

- "I want to know the status of order R-1001." → agent calls `lookup_account` then `list_rentals`.
- "Refund rental R-1002, the car broke down." → agent confirms verbally, calls `refund_rental`.
- "Get me a human." → agent calls `escalate_to_human`.

## Endpoints

```
GET  /health
POST /twilio/voice                          (Twilio webhook → returns TwiML)
WS   /twilio/stream                         (Twilio Media Streams WS)
GET  /sessions/sse                          (SSE: live list of active sessions)
GET  /sessions/{id}/events/sse              (SSE: live event stream for one session)
POST /sessions/{id}/kill                    (force-disconnect)
POST /sessions/{id}/clear                   (alias for kill — caller would reconnect for fresh session)
```

## What's deliberately NOT here

- **Auth on the Twilio webhook.** Real production should validate Twilio's `X-Twilio-Signature`.
- **Outbound calls.** Twilio trial restricts outbound to verified numbers; the demo is inbound-only.
- **`@rfnry/voice-client-react` audio hooks.** This dashboard only observes — it doesn't run a `VoiceSession` in the browser. The companion-assistant example exercises the React audio path.
- **Persistent storage.** `InMemoryVoiceStore` is used; sessions are gone on restart.
