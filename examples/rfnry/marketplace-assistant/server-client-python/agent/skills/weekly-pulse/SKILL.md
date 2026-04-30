---
name: weekly-pulse
trigger: user asks for "the weekly pulse", "last week's numbers", or any sales rollup
---

# Weekly Pulse

1. Call `SalesSummary` with `period="week"` (or `"month"` if the
   user asked monthly).
2. Call `RecentOrders` with `days=7` (or matching period).
3. Render two sections:
   - `## Sales Summary (<period>)` — units, revenue, top categories
     from the summary.
   - `## Recent orders (<n>)` — one bullet per order: `<id> —
     <status> — $<total> — <channel>`.

Don't analyze trends. Don't say "up from last week"; we don't have
the prior period's data on hand and you must not invent it.
