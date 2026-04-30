---
name: Shipping
description: Look up shipping status by tracking id. Returns carrier, status, last scan location, and estimated delivery days.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8201/shipping/{input.tracking_id}
  timeout: 10
input:
  tracking_id:
    type: string
    description: Carrier tracking id (TRK-XXX-NNNN format).
    required: true
---
