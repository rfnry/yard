# prefer-patch-over-rewrite

`ScribePatch` accepts structured edits — `line_replace`,
`regex_replace`, `rewrite` — applied to the seed content. `ScribeRewrite`
replaces the entire file body.

Patches are safer because:

- The model touches only what it explicitly names. Untouched lines
  stay byte-identical.
- The diff_summary in the response is small and reviewable.
- Whole-file rewrites are flagged in the event log as `mode: rewrite`,
  which is a risk signal for the compliance team's audit dashboard.

Use `ScribeRewrite` only when:

- The change is large enough that listing every line edit would be
  more error-prone than rewriting (rare).
- The user explicitly asked for a full restructure ("rewrite this in
  the new template format").

For numerical changes, identifier renames, or section additions:
`regex_replace` (with anchored patterns) or `line_replace` is almost
always the right tool.
