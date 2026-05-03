# analyst-assistant — data backend

Mock market-data API used by the analyst-assistant agent. No real data;
six fake companies with hardcoded snapshots and news headlines, just
enough to drive the agent through realistic tool-call sequences.

```
GET /companies                  list of {ticker, name, sector}
GET /companies/{ticker}         company profile
GET /market-snapshot/{ticker}   price, market cap, p/e, ytd change
GET /news/{ticker}              recent headlines
```

Run native:

```bash
cp .env.example .env
uv sync --extra dev
uv run poe dev          # listens on :8204
```

Or via the parent `docker-compose.yml`.
