---
name: litigation-team
leader: case-strategist
members:
  - records-investigator
  - filing-paralegal
mode: coordinate
share_member_context: true
max_delegations_per_turn: 5
---

# Litigation Team

A small litigation practice's case-handling team, scoped per `case_id`.
This team is what handles a matter **after** the intake-team has
cleared it through triage.

- **case-strategist** (leader) — receives the cleared matter, delegates
  to records-investigator for fact-finding and to filing-paralegal for
  any draft filings, synthesizes a closing memo. No tools of its own.
- **records-investigator** — owns the public-records HTTP tools
  (Identity, CriminalRecords, CourtRecords, PropertyRecords,
  BusinessRegistry, EmploymentHistory). Returns an
  `InvestigationReport`.
- **filing-paralegal** — owns filing-related tools (CourtForms,
  StatuteLookup) and produces a `FilingReview` when a draft filing is
  needed.

Cross-case isolation is structural: every member's data writes go to
`data/<case_id>/...` under the team root, with the path-jail
enforcing the boundary.

Cross-member context lives in `data/<case_id>/CONTEXT.md` (via
`share_member_context: true`). The leader records what it has already
delegated this turn so it doesn't double-pull.
