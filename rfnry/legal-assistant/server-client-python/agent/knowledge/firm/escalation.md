# Escalation

Surface to the lead attorney rather than burying in the report when:

- A subject's `CriminalRecords` includes a federal charge active in
  the last 24 months. (The lawyer needs to know whether parallel
  proceedings affect strategy.)
- `BusinessRegistry` shows the subject as a principal of an entity
  that is also a party to an active case the firm is handling.
  This is a conflict trigger; flag it before continuing.
- A property lookup returns a deed dated within 90 days of the
  matter's filing date — recent transfers can indicate asset
  sheltering.
- Any lookup returns explicitly anonymized juvenile content with a
  case number that overlaps the matter's docket. This is a
  redaction-handling issue, not a finding to report.

The escalation path is the report's `Followups` line, not a
separate channel — the attorney reads the report; flagging there
is sufficient.
