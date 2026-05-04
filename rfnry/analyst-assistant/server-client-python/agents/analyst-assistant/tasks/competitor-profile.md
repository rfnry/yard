---
name: competitor-profile
---

# Competitor profile

Depth report on one company. Includes profile, snapshot, and a
chronological news rundown.

Procedure:

1. `company_profile(ticker)` — name, sector, founded, HQ.
2. `market_snapshot(ticker)` — full metrics.
3. `news(ticker)` — every headline returned.
4. Emit a `CompetitorProfile` with all fields filled where data exists.

Be honest about gaps: P/E may be null; headlines may be empty. Each
gap is a finding for the lead analyst.
