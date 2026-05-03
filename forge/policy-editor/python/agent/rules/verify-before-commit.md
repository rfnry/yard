# verify-before-commit

`ScribeVerify` runs the parser diff against the staged edit. It
returns: deletion paths, corruption paths, locked-field violations,
parse errors. **You must run it before every `ScribeCommit`.**

If verify reports `passed: false`:

1. Read the report carefully. The `structural_delta.deletion_paths`
   and `corruption_paths` tell you exactly what changed beyond what
   was asked.
2. Re-stage the edit (`ScribePatch` or `ScribeRewrite`) with the
   issue corrected.
3. Re-run `ScribeVerify`.
4. Only commit when `passed: true`.

Do **not** use `force: true` to push past a verify failure unless the
user explicitly asked for the value that triggered the violation. A
locked-field violation almost never warrants force — those fields are
locked because they're the part of the document where silent
corruption is most damaging.

If you cannot get verify to pass after a few tries, return the
`EditReport` with the failure recorded under `verify_failures` and
ask the user to clarify or confirm the change.
