# legal-assistant — rfnry agent + Team + Workflow example

An assistant for a small litigation practice. The example exercises
all three rfnry orchestration shapes against the same domain:

- **single agent** (`/turn`) — direct call to `records-investigator`.
- **team** (`/team/turn`) — `case-strategist` (leader) decides
  delegation dynamically across `intake-clerk` and `records-investigator`.
- **workflow** (`/workflow/run`) — fixed three-step pipeline:
  intake → records → strategist memo, with a condition branch.

Each `case_id` is a separate scope leaf — the rfnry path-jail makes
cross-case reads structurally impossible (no special agent
instruction needed; see "Path-jail" below).

## Single vs multi: how the substrate stacks

| Shape         | What you instantiate                                    | Filesystem                                                                                          |
|---------------|---------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Single agent  | `AgentEngine(root=<dir>)`                               | `<dir>/AGENT.md`, `<dir>/INDEX.md`, `<dir>/{rules,skills,tools,knowledge,tasks}/`                   |
| Team          | `Team(root=<parent>, name=X)`                           | `<parent>/agents/<each-member>/AGENT.md` + `<parent>/teams/X/TEAM.md`                              |
| Workflow      | `Workflow(root=<parent>, name=X)`                       | `<parent>/agents/<each-member>/AGENT.md` (+ optional `<parent>/teams/Y/`) + `<parent>/workflows/X/WORKFLOW.md` |

Agents are the leaves. A team is N leaves under one parent, plus a
TEAM.md naming the leader. A workflow is a deterministic graph over
leaves and/or teams. Same substrate, three composition shapes.

## The three agents

- **records-investigator** — owns the public-records HTTP tools
  (Identity, CriminalRecords, CourtRecords, PropertyRecords,
  BusinessRegistry, EmploymentHistory). Returns an
  `InvestigationReport`. This is the original legal-assistant agent
  from before the refactor; the directory is the same content moved
  into `agents/records-investigator/`.
- **intake-clerk** — classifies a free-form lawyer request into a
  structured JSON plan (subject_kind, subject_id, skill,
  specific_claims, notes). No public-records tools.
- **case-strategist** — team leader. No public-records tools. Reads
  the records-investigator's report and produces an opinion-free
  closing memo with **What we have / What we don't have / Suggested
  next moves**.

## Path-jail (what makes per-case isolation safe by construction)

`rfnry`'s `Scope` builder rejects values containing `/`, `\`, `..`,
`.`, or null bytes (so a case_id of `../bravo` cannot even be
constructed). `PathJail` then resolves every read/write target and
verifies it sits under one of the explicitly-approved roots. The
roots for a turn are the agent's markdown root and `data/<case_id>/`.

A team member trying to read another case's data — or the workflow
trying to splice across case_ids — gets `ScopeError` raised before
the filesystem call is made. The agents themselves don't need a "do
not cross cases" instruction — the kernel of the engine enforces it,
and that boundary survives uniformly across single-agent, team, and
workflow shapes.

## Layout

```
legal-assistant/
├── server-client-python/
│   ├── agents/                        the leaves (each is a full agent)
│   │   ├── records-investigator/      AGENT.md + INDEX.md + rules/skills/tools/knowledge/tasks
│   │   ├── intake-clerk/              AGENT.md + INDEX.md + rules + tasks/classify-request.md
│   │   └── case-strategist/           AGENT.md + INDEX.md + rules + tasks/synthesize-memo.md
│   ├── teams/
│   │   └── litigation-team/TEAM.md    leader=case-strategist, members=intake-clerk + records-investigator
│   ├── workflows/
│   │   └── client-intake/WORKFLOW.md  classify -> investigate -> condition -> synthesize
│   └── src/
│       ├── main.py                    builds AgentEngine + Team + Workflow on app.state
│       ├── routes.py                  /turn, /team/turn, /workflow/run, ...
│       ├── agent/                     single-agent path (records-investigator)
│       ├── team/                      Team(...) builder + run_team_turn
│       └── workflow/                  Workflow(...) builder + run_workflow / run_workflow_resume
├── data-backend/                      mock public-records HTTP backend (port 8203)
└── docker-compose.yml
```

The same agent `records-investigator` participates in all three
shapes — a single AGENT.md is reused under three composition layers
without copy-paste.

## Run with Docker Compose

```bash
docker compose up -d
docker compose logs -f
```

## Run native (no docker)

```bash
# terminal 1
cd data-backend && uv sync --extra dev && uv run poe dev      # 8203

# terminal 2
cd server-client-python && cp .env.example .env && uv sync --extra dev && uv run poe dev   # 8102
```

## Endpoints

```
# single agent — records-investigator alone
POST /turn                  { "session_id":"...", "case_id":"...", "message":"...", "task":"investigate" }
POST /resume                { "session_id":"...", "case_id":"..." }
POST /consolidate           { "case_id":"...", "task":"investigate" }
POST /optimize/skill        { "case_id":"...", "skill":"witness-profile", "task":"investigate" }

# team — case-strategist leads dynamic delegation
GET  /team
POST /team/turn             { "session_id":"...", "case_id":"...", "message":"..." }

# workflow — deterministic three-step pipeline
POST /workflow/run          { "session_id":"...", "case_id":"...", "request":"..." }
POST /workflow/resume       { "session_id":"...", "case_id":"..." }

GET  /health
```

## Driving each shape

Same domain question, three call sites:

```bash
# 1) single agent — direct lookup
curl -X POST http://localhost:8102/turn \
  -H 'content-type: application/json' \
  -d '{"session_id":"s1","case_id":"alpha","message":"Pull what we have on witness ID-9876."}'

# 2) team — strategist orchestrates
curl -X POST http://localhost:8102/team/turn \
  -H 'content-type: application/json' \
  -d '{"session_id":"t1","case_id":"alpha","message":"Pull what we have on witness ID-9876, then summarize for me."}'

# 3) workflow — fixed pipeline
curl -X POST http://localhost:8102/workflow/run \
  -H 'content-type: application/json' \
  -d '{"session_id":"w1","case_id":"alpha","request":"Pull what we have on witness ID-9876, then summarize for me."}'

# inspect team roster
curl http://localhost:8102/team

# resume a workflow that crashed mid-step
curl -X POST http://localhost:8102/workflow/resume \
  -H 'content-type: application/json' \
  -d '{"session_id":"w1","case_id":"alpha"}'
```

The single-agent path produces an `InvestigationReport` (typed
output). The team and workflow paths produce a closing memo (string).

## When to pick which shape

- **Single agent** — one specialist, one tool catalog, one reply.
  Fastest, simplest, most direct.
- **Team** — when the routing decision is itself the model's job.
  The leader chooses what to delegate based on the request. Best for
  exploratory, free-form interactions.
- **Workflow** — when the pipeline is fixed and you want each step
  observable, retriable, and resumable from the event log. Best for
  batch ingest, scheduled jobs, anything you'd run from a cron.

The same three agents (intake-clerk, records-investigator,
case-strategist) sit under both the team and the workflow. The TEAM
runs them with a leader-decided delegation pattern; the WORKFLOW
runs them in a fixed 1-2-3 order with a condition branch.
