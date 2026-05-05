---
name: find-flights
---

# Find Flights

The primary task: pull a short comparable list of round-trip flights
for the requested origin/destination/date range, emit it as a
`FlightOptions` report.

A good outcome:

- Three to five options; under ten.
- Each option has carrier, total round-trip price (USD), depart/return
  durations, and any layover caveats.
- `notes` is empty unless the search came back empty or carriers are
  on a strike / advisory.
- The report parses on the first OutputSchema call (no retry).

A bad outcome:

- Inventing a price the tool didn't return.
- Returning ten near-duplicate options instead of the diverse three.
- Filling `notes` with chatter ("hope this helps").
