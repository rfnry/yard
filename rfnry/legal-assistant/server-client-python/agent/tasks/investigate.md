---
name: investigate
output_schema: InvestigationReport
---

# Investigate

The primary task: a lawyer working an active case (current scope is
the case_id) asks the assistant to pull and cross-reference public-
records data on a person, business, or court case.

The task is per-case. Reflections, outcomes, and lessons under this
task accumulate **only inside the active case_id's scope leaf** —
they never load into another case's boot bundle.

## Why refining matters here

Each case has its own habits — the names that recur, the kinds of
cross-checks the lawyer does most, the ID patterns that turn up
empty more often than not. After enough turns within a single case,
the consolidator distills those patterns into per-case lessons that
load into the boot bundle on the next turn for **that case only**.

A good outcome:

- Every fact in **Summary** came from a tool call this turn.
- **Sources** lists every tool with called/result-or-reason.
- "Not on file" / 404 results are surfaced, not glossed.
- No legal opinions, no strategy.
- Reflection captured what the lawyer was actually trying to do
  (witness profile vs cross-check vs case pull) and which lookups
  paid off.

A bad outcome:

- Hallucinated identity, criminal, or property facts.
- Implied judgment ("less credible", "stronger position").
- Skipped a tool the skill called for.
- Reused a fact from a prior turn without re-fetching.
