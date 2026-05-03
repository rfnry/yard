---
name: edit-policy
output_schema: EditReport
---

# Edit Policy

The primary (and only) task. The compliance team sends a request
phrased in natural language ("update X in Y from A to B", or "bump
X in Y AND update Z in W"); you execute the edit via the scribe
tool surface and return an `EditReport`.

For single-file requests, follow the `targeted-edit` skill. For
multi-file requests where the files must update consistently,
follow the `multi-file-edit` skill — the whole group commits
atomically, so verification must pass on every handle before any
file lands.

The task is per-policy. Each `policy_id` is a separate scope leaf —
files for policy A are never visible while you're working on policy B.

## A good outcome

- The user's request is restated in `request` (one line).
- Every file you read or wrote is listed in `files_touched`.
- `scribe_steps` records the exact sequence of operations, in order,
  with one entry per `Scribe*` tool call.
- `audit_ids` lists the `audit_id` from every successful commit.
- If verify failed at any point, the failure is captured in
  `verify_failures` (a short description per failure — do not omit
  failures even if you eventually succeeded).
- `summary` is one short paragraph in plain English describing what
  changed.

## A bad outcome

- A commit without a prior verify.
- A commit with `force: true` through a locked-field violation that
  the user did not ask for.
- A `ScribeRewrite` for a change that fits in one or two `line_replace`s.
- An edit that touches a file outside the user's stated request.
- An `EditReport` that omits scribe steps the model actually ran (the
  audit trail must reflect reality).
