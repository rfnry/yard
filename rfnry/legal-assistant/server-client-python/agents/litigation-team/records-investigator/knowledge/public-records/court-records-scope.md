# Court Records Scope

`CourtRecords` does **case-by-number** lookup, not subject-by-name.

Coverage:

- **Federal civil + criminal:** complete back to 1995.
- **State civil:** 38 states with searchable dockets; the rest
  return "docket text: unavailable, summary on file".
- **Juvenile:** redacted — case exists, parties are anonymized.

If you have a subject and need their cases, you must first call
`CriminalRecords` or another source to get case numbers, then call
`CourtRecords` per number. There is no "list cases by party name"
endpoint.

A 404 means the case number was not found. A 200 with
"docket text: unavailable" means the case exists but the source
doesn't have full text — surface the summary fields and note the
gap.
