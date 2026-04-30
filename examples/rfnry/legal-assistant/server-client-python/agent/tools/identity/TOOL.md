---
name: Identity
description: Government identity record by person id. Returns full name, DOB, address, ssn_last4, issued ID type.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8200/legal-assistant/identity/{input.person_id}
  timeout: 10
input:
  person_id:
    type: string
    description: Person id (ID-NNNN format).
    required: true
---
