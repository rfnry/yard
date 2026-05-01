---
name: weekly-summary
output_schema: WeeklySummary
---

# Weekly summary

A one-screen briefing across the client's tracked tickers. The client's
question names the tickers; you don't pick them.

Procedure:

1. For each named ticker: `market_snapshot` + `news`.
2. Identify the biggest YTD mover (positive or negative).
3. Identify any ticker with news in the last 14 days.
4. Emit a `WeeklySummary` with the rollup.

Don't pull `company_profile` here unless the client specifically asks
for sector context — that's `competitor-profile`'s job. Keeping the
weekly summary cheap matters; the client runs this every Monday.
