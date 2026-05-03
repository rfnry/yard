# companion-assistant — voice companion (WebRTC + OpenAI Realtime)

Samantha-from-*Her* style. Browser-only. Talk naturally with a voice companion who remembers the active conversation and proactively re-engages after a stretch of silence.

This example exercises the full **client-side** voice stack: `@rfnry/voice-client-react` hooks + `<FrequencyVisualizer mode="circular" />`, WebRTC negotiation against `WebRTCTransport` from `rfnry-voice-server[webrtc]`. It does **not** depend on `rfnry`, `rfnry-chat`, or any telephony adapter.

## Layout

```
companion-assistant/
├── server-python/          FastAPI + WebRTC signaling (port 8401)
│   └── src/
│       ├── main.py         app + memory init
│       ├── routes.py       POST /webrtc/offer/{user_name}
│       ├── memory.py       per-user in-process conversation memory
│       ├── nudges.py       SilenceNudger — sends a re-engagement prompt after silence
│       └── agent.py        STS provider + instructions template (companion + user + memory)
└── client-react/           Vite app (port 5174)
    └── src/
        ├── app.tsx         onboarding → session
        ├── onboarding.tsx  name entry
        └── session.tsx     <FrequencyVisualizer mode="circular" /> + connect/mute
```

## Run with Docker Compose

```bash
cp server-python/.env.example server-python/.env  # set OPENAI_API_KEY
docker compose up
```

Open <http://localhost:5174>. Server: <http://localhost:8401>.

## Run native

```bash
# terminal 1
cd server-python && uv sync --extra dev && uv run poe dev

# terminal 2
cd client-react && npm install && npm run dev
```

## Use it

1. Open <http://localhost:5174>.
2. Allow mic when the browser prompts.
3. Enter your name (alphanumeric) + the companion's name (default: `Sam`).
4. Click **start**, then **talk to Sam**.
5. Speak. Sam responds with WebRTC-quality audio. Frequency visualizer pulses with both your and Sam's voice.
6. Stay silent for ~25 seconds. Sam will start the conversation back up.
7. Click **end** to disconnect.

## What the example tests

- **WebRTC client + server end-to-end** (`@rfnry/voice-client-react` + `WebRTCTransport`).
- **STS mode** (OpenAI Realtime) without telephony in the loop.
- **Memory templating** — every transcript turn appended to `CompanionMemory`; instruction template includes recent turns + summary on every new connect.
- **Proactive re-engagement** via `SilenceNudger` injecting a system text after silence.
- **Circular FFT visualizer** — agent's amplitude pulses the central orb radius; halo bars driven by user + agent frequency bins.

## Caveats

- **Memory is in-process.** Reboot wipes it. This is intentional — the example proves the loop, not durable storage.
- **No auth.** This is a demo. Real production gates `/webrtc/offer/{user_name}` with whatever the host uses.
- **STUN only** — uses Google's public STUN. Behind symmetric NAT you'll need TURN; configure via `<VoiceProvider iceServers={...}>` in `app.tsx`.
- **The nudger** is wired conservatively — sends through the STS session if available; if the integration can't grab the STS session handle, nudges are a no-op (the rest of the app still works).
