# targeted-edit

The canonical procedure for any policy-document edit.

## Steps

1. **Identify the file.** Map the user's request to a single file
   under the active policy_id. If multiple files are involved, do
   one at a time; the report records each.

2. **`ScribeRead(path)`.** Returns a `handle_id`, the parser used
   (`json`, `markdown`, `plain_text`, ...), the structure (element
   counts), and `locked_fields` — paths the parser auto-locked
   (typically numeric leaves in JSON, all headings in markdown).

3. **Plan the patch.** Pick the smallest edit kind that expresses
   the change:
   - Numeric or string substitution: `regex_replace` with an
     **anchored** pattern (include surrounding context so the regex
     matches exactly one location).
   - Line-targeted change: `line_replace` with the 1-based line
     number from your read.
   - Section addition: `regex_replace` that matches the heading
     before the insertion point and replaces it with `heading +
     new section + heading`.

4. **`ScribePatch(handle_id, edits=[...])`.** Stages the edit. The
   response includes a `diff_summary` (bytes/lines delta).

5. **`ScribeVerify(handle_id)`.** Run the parser diff. Read the
   report:
   - `passed: true` — proceed to commit.
   - `passed: false` with `locked_field_violations: [...]` — you
     changed a field the parser auto-locked. Re-stage with the
     correct value (or confirm with the user) and re-verify.
   - `passed: false` with `deletion_paths: [...]` — your patch
     removed structural elements. Re-stage to restore them.
   - `passed: false` with `parse_error: ...` — your patch produced
     invalid syntax (broken JSON, etc.). Re-stage with corrected
     syntax.

6. **`ScribeCommit(handle_id)`.** Persists the staged edit. Returns
   `audit_id`. Record this in the `EditReport`.

## Anti-patterns

- Calling `ScribeRewrite` to make a one-line change.
- Calling `ScribeCommit` without a prior `ScribeVerify`.
- Passing `force: true` because verify "is being annoying."
- Editing a file you didn't `ScribeRead` this turn (handles don't
  persist across turns).
