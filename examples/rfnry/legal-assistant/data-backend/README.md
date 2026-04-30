# data-backend — legal-assistant mock data

Standalone FastAPI server (port `8203`) serving deterministic mock
public-records data for the legal-assistant agent's HTTP tool calls.

## Endpoints

```
GET /identity/{person_id}                 government identity
GET /criminal-records/{person_id}         conviction history
GET /court-records/{case_number}          court case lookup
GET /property-records/{person_id}         real estate
GET /business-registry/{business_id}      entity formation + principals
GET /employment-history/{person_id}       declared employment
GET /health
```

## Run

```bash
cd yard/examples/rfnry/legal-assistant/data-backend
cp .env.example .env
uv sync --extra dev
uv run poe dev          # http://127.0.0.1:8203
```
