# INDEX

Map of this agent's tree.

## Identity & shape

- `AGENT.md` — persona, reply contract, hard rules.
- `INDEX.md` — this file.

## Rules (always-on guidance)

- `rules/_index.md` — list of active rules.
- `rules/verify-before-commit.md` — verify is mandatory; force is a manual override.
- `rules/prefer-patch-over-rewrite.md` — patch beats rewrite for partial edits.

## Skills (procedures the model can `Skill`-load)

- `skills/_index.md` — list.
- `skills/targeted-edit.md` — single-file edit loop.
- `skills/multi-file-edit.md` — atomic multi-file edit loop.

## Tasks

- `tasks/edit-policy.md` — the only task.

## Tools (provided programmatically by the host)

Single-file:
- `ScribeRead`, `ScribePatch`, `ScribeRewrite`, `ScribeVerify`, `ScribeCommit`

Multi-file (atomic group):
- `ScribeReadGroup`, `ScribeVerifyGroup`, `ScribeCommitGroup`,
  `ScribeDiscardGroup`

Registered programmatically through `scribe_tools()`; not declared
as markdown tool files because they're typed Python `Tool`
subclasses with rich Pydantic input models.
