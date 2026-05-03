# support-assistant — server-python

FastAPI server hosting a `rfnry-voice-server` STS session per Twilio call. Tools hit an in-memory rentals/accounts/returns dataset.

## Run

```bash
uv sync --extra dev
cp .env.example .env  # set OPENAI_API_KEY + PUBLIC_HOST
uv run poe dev        # listens on :8301
```

See the parent `README.md` for the full Twilio + cloudflared playbook.
