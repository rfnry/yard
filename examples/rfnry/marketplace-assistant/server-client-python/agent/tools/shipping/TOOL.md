---
name: Shipping
description: Tracking status by tracking id. Returns carrier, status, last_scan_location, estimated_delivery_days.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8200/marketplace-assistant/shipping/{input.tracking_id}
  timeout: 10
input:
  tracking_id:
    type: string
    description: Tracking id in the form MKT-TRK-NNNNN.
    required: true
---
