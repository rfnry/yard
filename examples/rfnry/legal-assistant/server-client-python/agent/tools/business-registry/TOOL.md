---
name: BusinessRegistry
description: Business-entity record by business id. Returns legal_name, state_of_formation, registered_agent, principals, active flag.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8203/business-registry/{input.business_id}
  timeout: 10
input:
  business_id:
    type: string
    description: Business id (e.g. BIZ-NHB-01).
    required: true
---
