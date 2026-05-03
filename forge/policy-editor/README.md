# policy-editor — rfnry + forge-scribe example

A compliance-team assistant that edits internal policy documents
under custody. Each `policy_id` is a separate scope leaf — the rfnry
path-jail makes cross-policy edits structurally impossible (no
special agent instruction needed).

The agent uses **forge-scribe** as its only edit surface. Every
modification flows through `read → patch → verify → commit`, with a
strict commit policy that refuses on parser-detected deletion,
corruption, or locked-field violation. The agent only writes to disk
*after* verify passes.

Two edit shapes are exercised:

- **Single-file edit** — the standard flow when one document changes.
- **Atomic multi-file edit** — when a request requires consistency
  across multiple files (e.g. bumping `retention.json`'s version
  *and* updating `parental-leave.md`'s duration in one logical
  policy change). The whole group commits together via Phase A→B
  write-then-rename: either every file is updated, or none are.

## Why this example

This is the smallest end-to-end test of `rfnry` + `rfnry-forge-scribe`
working together. It exercises:

- The five scribe operations as rfnry-native tools (via
  `scribe_tools()`).
- Path-jail integration — read/write roots come from rfnry; scribe
  uses them transparently.
- Verify-fail-then-fix loop — the parser report is fed back to the
  model so it can correct its own staged edit before committing.
- Per-policy scope isolation — handles, lessons, and edits never
  leak between `policy_id`s.

## Layout

```
policy-editor/
├── seeds/                     starter policy documents
├── python/
│   ├── agent/                 markdown agent tree (AGENT, INDEX, rules, skills, tasks)
│   └── src/                   FastAPI server + Agent wiring
└── docker-compose.yml         (none — runs natively, no infra)
```

## Run

```bash
cd python
cp .env.example .env       # set ANTHROPIC_API_KEY
uv sync --extra dev
uv run poe dev             # 8104
```

## Endpoints

```
POST /init     { "policy_id": "leave-2026" }
               copies seed files into data/<policy_id>/ for the agent to edit

POST /turn     { "session_id": "...", "policy_id": "...", "message": "..." }
               agent reads, patches, verifies, commits via scribe

POST /list     { "policy_id": "..." }
               returns the current state of policy files in the scope

GET  /health
```

## Example session — single file

```bash
curl -sX POST http://localhost:8104/init \
  -H 'content-type: application/json' \
  -d '{"policy_id": "leave-2026"}'

curl -sX POST http://localhost:8104/turn \
  -H 'content-type: application/json' \
  -d '{
    "session_id": "s1",
    "policy_id": "leave-2026",
    "message": "Update parental-leave.md: change the leave duration from 12 weeks to 16 weeks. Keep all other content."
  }'
```

## Example session — atomic multi-file

```bash
curl -sX POST http://localhost:8104/turn \
  -H 'content-type: application/json' \
  -d '{
    "session_id": "s2",
    "policy_id": "leave-2026",
    "message": "Update parental-leave.md to 16 weeks AND bump retention.json version from 3 to 4 to mark this policy change. Both must commit together — either both go through or neither does."
  }'
```

The agent picks `ScribeReadGroup` for this request, stages an edit
on each file, runs `ScribeVerifyGroup`, and commits with
`ScribeCommitGroup`. The returned `EditReport` shows
`mode: "group"`, both files in `files_touched`, and a single
`audit_id` for the atomic commit.

## What corruption looks like in this example

The seed `retention.json` has numeric leaf fields (`days`, `version`).
forge-parser auto-locks these. If the model tries to silently change
`retention_days: 90` → `retention_days: 900`, scribe's `verify` flags
a `locked_field_violation` and the strict commit policy refuses. The
model receives the report and can correct the staged edit before
re-committing.

## Notes

- Single-process, single shared `Scribe` instance across turns.
  Concurrent turns on different policy_ids are safe (handles are
  unique per read), but two concurrent turns on the *same* policy_id
  will see shared handle state. For production, instantiate one
  `Scribe` per session.
- No `refining` is configured — this example focuses on the edit loop
  itself, not on the agent self-evolving. Add `RefiningConfig(...)`
  the same way `legal-assistant` does to extend it.
