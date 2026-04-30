# legal-assistant — rfnry agent example

An assistant that helps a small litigation practice work through
cases. Each `case_id` is a separate scope leaf — the rfnry path-jail
makes cross-case reads structurally impossible (no special agent
instruction needed; see "Path-jail" below).

The agent leans heavily on **refining**:
- Per-case reflections after every turn capture what the lawyer
  asked, what the assistant looked up, and what was missing.
- Lessons consolidate the patterns that repeat across turns *within
  one case*, so the assistant's understanding of that case sharpens
  with use.
- Lessons from case A never leak to case B — the path-jail extends
  to the lessons directory.

## Path-jail (what makes this safe by construction)

`rfnry`'s `Scope` builder rejects values containing `/`, `\`, `..`,
`.`, or null bytes (so a case_id of `../bravo` cannot even be
constructed). `PathJail` then resolves every read/write target and
verifies it sits under one of the explicitly-approved roots — the
roots for a turn are `agent_root/...` (the markdown tree) and
`data/<case_id>/...`. A tool trying to read another case's data
gets `ScopeError` raised before the filesystem call is made.

The agent itself doesn't need a "do not cross cases" instruction —
the kernel of the engine enforces it.

## Run with Docker Compose

```bash
docker compose up -d
docker compose logs -f
```

Service: `agent` (port `8102`). Requires `backend` (port `8200`).

## Endpoints

```
POST /turn       { "session_id":"...", "case_id":"...", "message":"...", "task":"investigate" }
POST /resume     { "session_id":"...", "case_id":"..." }
GET  /health
```
