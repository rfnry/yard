---
name: EmploymentHistory
description: Declared employment history for a person id. Returns a list of {employer, role, from, to (or null if current)}.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8203/employment-history/{input.person_id}
  timeout: 10
input:
  person_id:
    type: string
    description: Person id (ID-NNNN format).
    required: true
---
