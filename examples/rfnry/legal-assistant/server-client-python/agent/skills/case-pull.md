---
name: case-pull
trigger: lawyer asks for a court record by case number, or names a docket number
---

# Case Pull

1. `CourtRecords(case_number)` — fetch the case record (court,
   parties, filed_at, closed_at, outcome).
2. For each named party that looks like a person id (ID-NNNN), call
   `Identity` to confirm.
3. For each named party that looks like a business id, call
   `BusinessRegistry`.
4. Render under `## <case_number>` — case details first, then a
   sub-bullet list of parties with their identity/registry summaries.
