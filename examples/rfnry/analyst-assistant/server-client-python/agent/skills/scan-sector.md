# Skill — scan the sector

Use when the client asks "what's moving" without naming a ticker.

Sequence:

1. `companies()` — list the full coverage universe.
2. For each ticker, `market_snapshot(ticker)` — collect YTD change.
3. Rank by absolute YTD change; pull `news` for the top 2 movers.

Report the movers. Don't pull news for tickers without significant
movement — that's wasted budget.
