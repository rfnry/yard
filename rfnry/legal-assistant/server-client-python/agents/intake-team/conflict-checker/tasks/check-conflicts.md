---
name: check-conflicts
---

# Check Conflicts

Query the conflicts database for the named parties and return a
structured `ConflictCheck` verdict.

A good outcome:

- One DB query per named party (no skipping, no extra invented ones).
- Verdict mapping follows `rules/verdict-strict-mapping.md`.
- Report parses on the first OutputSchema call.

A bad outcome:

- Skipping the DB call and "inferring" a verdict.
- Returning `direct_conflict` without an `opposing` row in
  `parties_checked`.
- Filling `notes` for a `clear` verdict.
