# companion-assistant — client-react

Browser UI for the companion-assistant. Onboarding asks for your name + the companion's name, then opens a WebRTC session against the server.

```bash
npm install
cp .env.example .env  # set VITE_VOICE_SERVER_URL
npm run dev           # listens on :5174
```

The audio + visualizer + transport negotiation are all handled by `@rfnry/voice-client-react`. This app is just the onboarding form + a `<Session>` component composing `<FrequencyVisualizer mode="circular" />` and `useVoiceSession()`.
