---
name: quote-lookup
---

# Quote Lookup

The primary task: take a user message asking about one or more stock
tickers and return the current prices via the `Quote` tool.

A good outcome:

- Every quoted price came from a `Quote` call in this turn.
- Output format is consistent: `<TICKER>: $<price> <currency>`.
- For multiple tickers, the agent calls `Quote` once per ticker rather
  than guessing.

A bad outcome:

- Fabricated prices (no `Quote` call in the transcript).
- Stale prices from a previous turn.
- Analysis or recommendations beyond the raw quotes.
