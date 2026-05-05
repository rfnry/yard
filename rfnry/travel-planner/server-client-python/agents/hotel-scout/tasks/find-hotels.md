---
name: find-hotels
---

# Find Hotels

Find lodging matching the budget band, surface review-pattern red
flags, emit a `HotelOptions` report.

A good outcome:

- Three to five options.
- Each entry has name, neighborhood, nightly rate, total, rating,
  one-line review-pattern summary.
- Red-flag caveats are on the entry, not buried in `notes`.
- Report parses on the first OutputSchema call.

A bad outcome:

- Listing only the top-rated three; the synthesizer wants a price
  spread.
- "Quiet location" without saying which neighborhood.
- Quoting only nightly without the total — the synthesizer compares
  totals across scouts.
