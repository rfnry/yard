---
name: witness-profile
trigger: lawyer asks for "what we have on" or "a profile of" a person id (ID-NNNN)
---

# Witness Profile

Full sweep on one person:

1. `Identity(person_id)` — basic identity record.
2. `CriminalRecords(person_id)` — convictions + dispositions.
3. `PropertyRecords(person_id)` — real estate on file.
4. `EmploymentHistory(person_id)` — declared employment.

If the identity record names a business or the lawyer mentioned
one, also call `BusinessRegistry(business_id)`. If the criminal
records reference a case number, optionally call `CourtRecords` for
the most recent one.

Render under `## <Full Name> (<person_id>)`. Each tool result gets a
**Summary** sentence and a **Sources** row. Skipped tools get a
"called: no" row with the reason.
