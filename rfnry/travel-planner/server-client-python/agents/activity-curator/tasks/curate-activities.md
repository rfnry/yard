---
name: curate-activities
---

# Curate Activities

Pick a balanced list of activities for the trip duration matching the
stated mood. Return an `ActivityList` report.

A good outcome:

- One anchor experience per day max, plus self-paced options.
- Each entry: name, day (1-indexed), duration_hours, per-person price,
  ticketed (bool), one-line "why this fits the mood" summary.
- "Relaxing" mood: at least one half-day is intentionally unscheduled
  with a `caveats` note saying so.
- Report parses on first OutputSchema call.

A bad outcome:

- Filling every slot — overscheduling defeats the synthesizer's
  attempt to compose a real itinerary with travel time + meals.
- Recommending an activity outside the date range.
- Quoting prices without specifying per-person vs per-group.
