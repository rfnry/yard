---
name: CourtRecords
description: Court case record by case number. Returns court, case_type, filed_at, closed_at, parties, outcome.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8203/court-records/{input.case_number}
  timeout: 10
input:
  case_number:
    type: string
    description: Court case number (e.g. OR-2014-CRM-04412, MA-2024-CIV-99012).
    required: true
---
