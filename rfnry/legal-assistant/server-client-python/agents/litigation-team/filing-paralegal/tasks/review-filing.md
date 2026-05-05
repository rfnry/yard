---
name: review-filing
---

# Review Filing

Review a draft filing. Return a `FilingReview`.

A good outcome:

- `procedural_issues`, `missing_exhibits`, `citation_issues` lists each
  derived from a tool call (no inferred ones).
- `verdict` follows the mapping in `rules/verdict-mapping.md`.
- `ready_to_file` only when all three lists are empty.
- Report parses on the first OutputSchema call.

A bad outcome:

- `ready_to_file` with non-empty issue lists.
- Inferring "missing" exhibits without `CourtForms` confirming.
- Drafting in response to a draft request.
