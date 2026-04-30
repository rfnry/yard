---
name: PropertyRecords
description: Real-estate records for a person id. Returns a list of properties (address, ownership type, since-date, tax-assessed value).
executor: http
config:
  method: GET
  url: http://127.0.0.1:8203/property-records/{input.person_id}
  timeout: 10
input:
  person_id:
    type: string
    description: Person id (ID-NNNN format).
    required: true
---
