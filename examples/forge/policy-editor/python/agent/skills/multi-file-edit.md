# multi-file-edit

The procedure for any policy edit that spans more than one file
and requires the files to be updated together.

## When to use this instead of `targeted-edit`

Use multi-file-edit when:

- Two or more files reference each other (e.g., a version field in
  `retention.json` is bumped because a duration changed in
  `parental-leave.md`).
- A single logical policy change requires consistent state across
  the file set (a partial commit would leave the policies
  inconsistent).
- The user phrased the request with "and" / "both" / "together":
  *"raise leave to 16 weeks **and** bump retention version"*.

If the request fits in a single file, use `targeted-edit` instead —
the group machinery has overhead that's only worth it for genuine
atomicity needs.

## Steps

1. **Read all files at once.** `ScribeReadGroup(paths=[...])`
   returns a `group_id` and per-file handle summaries. Every handle
   in the group commits together; you cannot commit half of them.

2. **Stage edits per handle.** Use the regular `ScribePatch` /
   `ScribeRewrite` against each `handle_id`. Edits are independent
   at the staging step — patching one handle doesn't affect another.
   Re-staging a handle clears any prior verify report for the group.

3. **`ScribeVerifyGroup(group_id)`.** Returns one report covering
   the whole group:
   - `passed: bool` — true only if every handle is staged AND
     every per-handle verify passes.
   - `handle_reports: dict[handle_id, VerifyReport]` — same shape
     as a single-file `verify` report, one entry per handle. Use
     this to find which handle failed and how.
   - `unstaged_handles: list[handle_id]` — handles in the group
     with no staged edit. The group can't commit until every
     handle is staged.

4. **Fix and re-verify.** If `passed: false`:
   - For each entry in `handle_reports` with `passed: false`,
     re-stage that specific handle with the issue corrected.
   - Re-run `ScribeVerifyGroup`. The same group_id stays valid —
     you don't need to re-read.
   - Don't `ScribeDiscardGroup` unless you're abandoning the work
     entirely; restaging is cheaper.

5. **`ScribeCommitGroup(group_id)`.** Atomically writes all files.
   Either every file is updated or none are. The commit returns
   one `audit_id` covering the whole group — record it in the
   `EditReport`.

6. **If commit refuses,** the agent receives a single rejection
   reason listing each failing handle. Fix the staged edits and
   retry — do not pass `force=true` unless the user explicitly
   authorized the flagged change.

## Anti-patterns

- Reading files individually (`ScribeRead` for each) when the
  request needs atomicity. Without a group, a mid-sequence failure
  leaves partial state on disk.
- Calling `ScribeCommit` (single-handle) on a handle that came
  from `ScribeReadGroup`. The single commit routes through the
  group anyway, which means it tries to commit *all* handles in
  the group — which can fail if other handles aren't staged. Use
  `ScribeCommitGroup` explicitly to make the intent clear.
- Ignoring `unstaged_handles` in the verify report. If a handle is
  in the group, the agent must either stage it or `ScribeDiscardGroup`
  and start over.
- Passing `force=true` to push past a multi-handle verify failure.
  The risk surface is per-file; forcing a group force-commits
  every flagged handle.

## Example

User: *"Update parental leave from 12 weeks to 16 weeks AND bump
retention.json version from 3 to 4 to mark the policy change."*

```
ScribeReadGroup(paths=["parental-leave.md", "retention.json"])
  → group_id=g_abc, handles=[{handle_id: h1, path: parental-leave.md},
                              {handle_id: h2, path: retention.json}]

ScribePatch(handle_id=h1, edits=[regex_replace 12 weeks → 16 weeks])
ScribePatch(handle_id=h2, edits=[json_patch replace /version 3 → 4])

ScribeVerifyGroup(group_id=g_abc)
  → passed: false (retention.json: locked_field_violations=['version'])

  # version is locked; the user explicitly asked to bump it, so this
  # is one of the rare cases where force=true is appropriate.

ScribeCommitGroup(group_id=g_abc, force=true)
  → committed: true, audit_id: edit_xyz
```

The `EditReport` records:
- `files_touched`: `[parental-leave.md, retention.json]`
- `audit_ids`: `[edit_xyz]` (one ID for the whole group)
- `verify_failures`: `[retention.json: locked_violations=['version']]`
  (preserved even though the eventual commit succeeded with force)
