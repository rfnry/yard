---
name: Order
description: Look up an order by id. Returns channel (web|amazon|wholesale), skus, status, tracking_id, payment_id, total, placed_at.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8202/orders/{input.order_id}
  timeout: 10
input:
  order_id:
    type: string
    description: Order id in the form MKT-NNNNN.
    required: true
---
