# therapy-assistant

## Get Started

```bash
cd examples/knowledge/therapy-assistant

docker compose up -d

cd python
cp .env.example .env
uv sync --extra dev
uv run poe dev
```

## Testing

```bash
curl -X POST http://localhost:8202/chat \
  -H 'content-type: application/json' \
  -d '{"memory_id":"alex","message":"I just moved to Lisbon and I feel a bit lost."}'
```

```bash
curl -X POST http://localhost:8202/chat \
  -H 'content-type: application/json' \
  -d '{"memory_id":"alex","message":"Where did I say I moved to?"}'
```
