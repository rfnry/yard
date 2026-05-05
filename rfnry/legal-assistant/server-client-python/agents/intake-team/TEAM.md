---
name: intake-team
leader: intake-coordinator
members:
  - intake-clerk
  - conflict-checker
mode: coordinate
share_member_context: true
max_delegations_per_turn: 5
---

# Intake Team

The team that decides whether a new matter even gets opened.

- **intake-coordinator** (leader) — reads the lawyer's free-form
  intake, decides whether to delegate to clerk + conflict-checker,
  and produces an `IntakeReport` saying go / no-go / needs-more-info.
- **intake-clerk** — classifies the request into a structured plan
  (subject_kind, subject_id, skill, specific_claims). No
  conflict-checking authority.
- **conflict-checker** — runs the conflict-of-interest checks against
  the `ConflictDatabase` tool. Returns a structured verdict.

The leader does not call records / litigation tools — those belong to
the litigation-team. This team is gating: triage, classify, conflict
check, then either open the matter or refuse it.

The cross-team workflow at the repo root (`open-matter`) chains this
team's output into the litigation-team. If this team returns "no-go,"
the workflow stops here.

Cross-case isolation works the same as the litigation-team — every
member's data writes go to `data/<case_id>/...` under the team root,
path-jailed by construction.
