---
name: litigation-team
leader: case-strategist
members:
  - intake-clerk
  - records-investigator
mode: coordinate
share_member_context: true
max_delegations_per_turn: 5
---

# Litigation Team

A small litigation practice's investigative team, scoped per `case_id`.

- **case-strategist** (leader) — receives the lawyer's request,
  optionally delegates to intake-clerk for classification, delegates
  to records-investigator for the public-records work, synthesizes a
  closing memo. No tools of its own.
- **intake-clerk** — classifies a free-form request into a structured
  plan (subject_id, skill, specific_claims). No public-records tools.
- **records-investigator** — owns the public-records HTTP tools
  (Identity, CriminalRecords, CourtRecords, PropertyRecords,
  BusinessRegistry, EmploymentHistory). Returns an
  `InvestigationReport`.

Cross-case isolation is structural: every member's data writes go to
`data/<case_id>/...` under the team root, with the path-jail
enforcing the boundary. The team layer adds nothing here — the
substrate already does it.

Cross-member context lives in `data/<case_id>/CONTEXT.md` (via
`share_member_context: true`). The leader can use it to record what
it has already delegated this turn so it doesn't double-pull.
