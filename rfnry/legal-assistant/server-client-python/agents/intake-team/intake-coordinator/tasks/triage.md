---
name: triage
---

# Triage

Triage a new matter intake. Decide proceed / decline / needs_info.

A good outcome:

- `IntakeReport` parses on the first OutputSchema call.
- `classification` is the clerk's plan verbatim.
- `conflict_check` is the conflict-checker's verdict verbatim.
- `decision` follows the rules in `AGENT.md`.
- `rationale` is one paragraph and references the conflict result + the
  clarity of the classification.

A bad outcome:

- Inferring a conflict from prior knowledge.
- Calling `decline` without a direct conflict result from the checker.
- Stuffing the rationale with chatter unrelated to the decision.
