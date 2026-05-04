---
name: client-intake
input:
  case_id:
    type: string
    required: true
  request:
    type: string
    required: true
steps:
  - name: classify
    agent: intake-clerk
    input: "{workflow.input.request}"
  - name: investigate
    agent: records-investigator
    input: "Execute this investigation plan and return your standard InvestigationReport. Plan:\n\n{classify.output}"
  - name: route_followups
    condition: "investigate.output contains 'not on file'"
    then:
      - name: synthesize_thin
        agent: case-strategist
        input: "Read the investigation findings below. The investigator surfaced 'not on file' on at least one lookup, so your **What we don't have** section is load-bearing. Compose the closing memo.\n\nClassification:\n{classify.output}\n\nFindings:\n{investigate.output}"
    else:
      - name: synthesize_full
        agent: case-strategist
        input: "Read the investigation findings below and compose the closing memo.\n\nClassification:\n{classify.output}\n\nFindings:\n{investigate.output}"
output: "{route_followups.output}"
---

# Client Intake Workflow

Deterministic three-step pipeline:

1. **classify** — `intake-clerk` reads the free-form lawyer request
   and emits a structured JSON plan.
2. **investigate** — `records-investigator` executes the plan via
   public-records lookups, returns an `InvestigationReport`.
3. **route_followups** — branches on whether the investigation
   surfaced any "not on file" results:
   - **then** branch (`synthesize_thin`): the investigator hit a
     gap; the case-strategist memo's **What we don't have** section
     is load-bearing.
   - **else** branch (`synthesize_full`): everything came back; the
     memo's main weight is in **What we have** and **Suggested next
     moves**.

The condition is a string-`contains` check on the investigation
output — coarse, but enough to demonstrate the branching primitive.
A real production workflow would have the records-investigator emit
a structured report and condition on a typed field.

The same three agents are also wired as a `litigation-team` (see
`teams/litigation-team/TEAM.md`). Use the workflow when you want a
fixed, observable, resumable pipeline; use the team when you want
the strategist to decide delegation dynamically.
