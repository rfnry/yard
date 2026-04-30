---
name: summarize-portfolio
trigger: user lists multiple tickers and asks for an overview
---

# Summarize Portfolio

When the user lists 2 or more tickers and asks for an overview:

1. Call `Quote` once per ticker — sequentially, not in parallel.
2. Sum the returned prices to produce a "naive total" (one share each).
3. Reply with one line per ticker (`AAPL: $189.42 USD`) followed by
   the total. No analysis, no recommendations — quotes only.
