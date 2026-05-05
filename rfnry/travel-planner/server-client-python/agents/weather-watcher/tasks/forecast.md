---
name: forecast
---

# Forecast

Return a per-day forecast plus actionable advisories.

A good outcome:

- One row per trip day (`day_index`, `date`, `high_f`, `low_f`,
  `precip_pct`, `summary`).
- One to three concrete advisories that name a specific day.
- `confidence` on each row reflects horizon (high/medium/low).
- Report parses on the first OutputSchema call.

A bad outcome:

- Generic advisories ("dress in layers").
- Skipping days because the tool partially failed; mark the gap with
  `confidence: "low"` instead.
