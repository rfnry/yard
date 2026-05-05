---
name: synthesize-trip
---

# Synthesize Trip

Compose a single `TripPlan` from the four scout reports.

A good outcome:

- One flight chosen, one hotel chosen, both with one-line justifications.
- Per-day calendar with activities placed sensibly relative to the
  weather advisories.
- `cost_breakdown` math is correct and shown.
- `caveats` lists any non-trivial trade-offs (e.g. "moved kayak from
  day 3 to day 2 due to forecast").
- Report parses on the first OutputSchema call.

A bad outcome:

- Surfacing alternative flights/hotels — the traveler wanted a pick.
- Ignoring a weather advisory.
- Cost math that doesn't match the chosen flight × travelers + hotel
  total + ticketed activities.
- Empty `days` when the scouts gave consistent inputs (compose, don't
  punt).
