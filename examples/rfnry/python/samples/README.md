# Samples — real artifacts from a live run

This directory contains real filesystem artifacts produced by running the
`customer-support/self-evolving` example against Anthropic
(`claude-sonnet-4-6`) on **2026-04-20**. Three triage tickets were
processed, then `consolidate()` was called. Every file here was
**engine-written, not hand-crafted** — these are the exact bytes that
landed on disk.

```
samples/customer-support-self-evolving/
├── reflections/
│   ├── tkt1/1.md        pre-turn reflection (Level 1+)
│   ├── tkt2/1.md
│   └── tkt3/1.md
├── outcomes/
│   ├── tkt1/1.md        post-turn critic (Level 2+)
│   ├── tkt2/1.md
│   └── tkt3/1.md
├── learned/
│   ├── _index.md                    auto-loaded into next boot bundle
│   └── <timestamp>-<hash>.md ×3     consolidated instructions (Level 3)
└── consolidations/
    ├── <timestamp>.md               human-readable audit trail
    └── consolidations.jsonl         append-only event stream
```

## What to notice

### Reflections (`reflections/tkt2/1.md`, `tkt3/1.md`)

Each has YAML frontmatter with **engine-injected identity fields**
(`task`, `session`, `turn`, `at`, `pattern_hash`) and
**model-provided semantic fields** (`tags`, `citations`, `confidence`).
The `pattern_hash` is computed deterministically from the `Plan` section
by the engine before writing — the model never sees it. This is what
makes future consolidation possible.

### Outcomes (`outcomes/*/1.md`)

Every outcome carries `verdict`, `quality_score`, and inherits the
reflection's `pattern_hash`. The critic wrote substantive four-section
analyses grading the main turn against the reflection's plan.

Notice `outcomes/tkt1/1.md`: the reflection for that turn produced an
**empty body** (model quirk on the first call — confidence dropped to
the 0.3 cap because citations were empty). The critic still graded
the turn on its merits (quality 0.92) and explicitly noted the missing
plan in its **Verdict** section. This is the "graceful degradation"
property at work: reflection failure → main turn proceeds → critic
grades honestly.

### Learned (`learned/<ts>-<hash>.md`)

Three promoted instruction snippets, each synthesized by the consolidator
from a reflection+outcome pair. Engine-injected frontmatter points at
the evidence files. Body is model-authored, grounded in the paired
reflection.

One standout — `<ts>-e725ca287701478e.md` synthesized "Damaged-on-Arrival
Electronics Triage" — captures the Shipping policy clause citation
pattern, the 30-day refund window cross-reference, a safety-escalation
flag for hazardous materials, and the Grep-then-Read fallback pattern.
This is operational knowledge the agent **discovered from its own
runtime traces**, in three turns.

### Consolidation audit

`consolidations/<ts>.md` is the human-readable run log — which patterns
were promoted, which rejected, average quality per cluster.
`consolidations.jsonl` is the append-only event stream (one
`ConsolidationEvent` per `consolidate()` call).

## Caveats — honest notes

- **Thresholds were lowered for this demo.** `min_occurrences: 1` in the
  task's `reflection.promotion` config means every unique pattern
  promotes. Production would use 3+. With exact-hash clustering, real
  LLM output rarely aggregates at threshold 2+ because each reflection's
  Plan section varies slightly. **v4's semantic clustering** replaces
  exact-hash with embedding similarity and is what makes higher
  thresholds realistic.
- **Cost of this run**: three turns (reflection + main + critic each)
  plus one consolidation. Roughly $0.08 in Anthropic tokens on
  `claude-sonnet-4-6`.
- **These bytes are frozen in git.** Running the example yourself will
  produce different artifacts in `agents/customer-support/self-evolving/data/`
  (gitignored). To regenerate this snapshot, re-run the scripted flow
  and copy the resulting tree here.

## How to reproduce

```bash
cd examples/python
PROVIDER=anthropic ANTHROPIC_API_KEY=... uv run uvicorn server:app &

for msg in \
  "Customer received a broken vase. 12 days since delivery. What do I do?" \
  "Customer got a dented electronics box. 3 days old. They want a replacement." \
  "A customer says their delivered package looks damaged and they opened it to find broken items."
do
  curl -s localhost:8000/agents/customer-support/self-evolving/chat \
    -H 'content-type: application/json' \
    -d "$(jq -n --arg m "$msg" '{session_id:("tkt"+(now|tostring|split(".")[0])), message:$m, scope:{org_id:"acme"}, task:"triage"}')"
done

curl -s localhost:8000/agents/customer-support/self-evolving/consolidate \
  -H 'content-type: application/json' \
  -d '{"task":"triage","scope":{"org_id":"acme"}}'

# Then copy the tree:
cp -r agents/customer-support/self-evolving/data/acme/tasks/triage/. samples/customer-support-self-evolving/
```
