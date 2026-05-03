---
name: resolve-customer-issue
---

# Resolve Customer Issue

The primary task: a CS rep forwards a customer issue with their
framing notes; you investigate via tool calls and the policy
knowledge base, then return a three-section response (`Findings`,
`Recommendation`, `Open questions`).

A good outcome:

- Every fact in **Findings** is sourced from a tool call this turn
  or from a policy file under `knowledge/`.
- The recommendation is concrete (a 1–2 paragraph message the rep
  can relay) and consistent with the policies.
- Gaps are surfaced honestly under **Open questions** rather than
  papered over.
- The right skill fired (warped vs in-warranty defect vs refund
  vs status lookup).

A bad outcome:

- Hallucinated order ids, part numbers, warranty windows, or
  shipping ETAs.
- Generalized policy beyond what `knowledge/` actually says.
- Promised a partial refund or a custom expedite without supervisor
  authorization.
- Skipped a tool call because "it's probably fine."
