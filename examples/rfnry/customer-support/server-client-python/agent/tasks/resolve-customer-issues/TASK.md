---
name: resolve-customer-issues
---

# Resolve Customer Issues

The primary task: take an incoming customer message and resolve it in
one turn if possible, escalating cleanly if not.

A good outcome looks like:

- The customer's specific question is answered (no boilerplate).
- The order id is confirmed before any committing action.
- If the resolution touches a skill (`damaged-package`, `refund-request`),
  the skill's steps are followed in order — not paraphrased.
- If the request is outside scope, the agent escalates without inventing
  policy.

A bad outcome:

- Long apology before the answer.
- Promised something not in the skills (e.g., expedited shipping,
  partial refund, store credit, exception to the 30-day window).
- Took action without confirming the order id.
- Guessed at policy.
