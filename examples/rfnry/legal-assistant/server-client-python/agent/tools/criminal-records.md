---
name: CriminalRecords
description: Criminal-record history for a person id. Returns a list of records with case_number, offense, disposition, sentence, date.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8203/criminal-records/{input.person_id}
  timeout: 10
input:
  person_id:
    type: string
    description: Person id (ID-NNNN format).
    required: true
---
