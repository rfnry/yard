---
name: open-matter
input:
  case_id:
    type: string
    required: true
  client_name:
    type: string
    required: true
  matter_summary:
    type: string
    required: true
steps:
  - name: triage
    team: intake-team
    task: triage
    input: "New matter intake. Client: {workflow.input.client_name}. Summary: {workflow.input.matter_summary}."
  - name: should_proceed
    condition: "triage.output contains '\"decision\": \"proceed\"'"
    then:
      - name: investigate
        team: litigation-team
        task: investigate
        input: "The intake-team has cleared this matter. Triage report:\n\n{triage.output}\n\nProceed with investigation."
    else:
      - name: stop_here
        team: intake-team
        task: triage
        input: "The intake-team's prior triage was: {triage.output}. Echo the report back as the final workflow output (the matter is not proceeding to litigation)."
output: "{should_proceed.output}"
---

# Open Matter Workflow

Cross-team workflow that decides whether to open a new matter and, if
cleared, hands it off to the litigation-team.

1. **triage** — `intake-team` (leader: intake-coordinator) takes the
   free-form intake, delegates internally to intake-clerk + conflict-
   checker, and returns an `IntakeReport` with `decision: proceed |
   decline | needs_info`.
2. **should_proceed** — string-contains check on the intake report's
   decision field. (Coarse but enough to demonstrate the cross-team
   handoff; a real workflow would condition on a structured field.)
   - **then** branch (`investigate`): hand off to `litigation-team`
     (leader: case-strategist) which delegates to records-investigator
     and filing-paralegal as needed and returns its closing memo.
   - **else** branch (`stop_here`): echo the triage report back as the
     workflow output. The matter doesn't proceed.

This is the right shape for two teams: each team has a real leader
doing real coordination work; the workflow chains them with structured
output passing. Compare with `team:` blocks alone — neither team's
leader could call into the other team's members; the workflow is what
crosses that boundary cleanly.
