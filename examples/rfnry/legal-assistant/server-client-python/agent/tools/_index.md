# Tools

- **BusinessRegistry** — Business-entity record by business id. Returns legal_name, state_of_formation, registered_agent, principals, active flag.
- **CourtRecords** — Court case record by case number. Returns court, case_type, filed_at, closed_at, parties, outcome.
- **CriminalRecords** — Criminal-record history for a person id. Returns a list of records with case_number, offense, disposition, sentence, date.
- **EmploymentHistory** — Declared employment history for a person id. Returns a list of {employer, role, from, to (or null if current)}.
- **Identity** — Government identity record by person id. Returns full name, DOB, address, ssn_last4, issued ID type.
- **PropertyRecords** — Real-estate records for a person id. Returns a list of properties (address, ownership type, since-date, tax-assessed value).
