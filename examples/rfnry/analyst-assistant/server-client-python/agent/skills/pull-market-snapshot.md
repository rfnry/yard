# Skill — pull market snapshot

Use when the client asks about a single ticker and wants more than a
one-liner.

Sequence:

1. `companies(ticker)` — confirm the ticker is on file. If 404, stop and
   report.
2. `market_snapshot(ticker)` — price, market cap, P/E, YTD change.
3. `news(ticker)` — recent headlines.

Compose the report from those three calls. Don't infer trends from a
single snapshot — only state what the tool returned.
