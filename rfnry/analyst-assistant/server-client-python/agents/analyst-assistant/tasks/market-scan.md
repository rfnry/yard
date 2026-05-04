---
name: market-scan
---

# Market scan

A quick pulse on one ticker for the client. Two-paragraph synthesis,
not a deep dive.

Procedure:

1. Confirm the ticker is in coverage (`company_profile`).
2. Pull the snapshot (`market_snapshot`).
3. Pull recent news (`news`).
4. Emit a `MarketScan` with summary + one-line price commentary +
   sources.

If the ticker isn't on file, return a `MarketScan` with
`ticker_in_coverage=false`, an empty `headlines` list, and a
one-sentence summary saying so.
