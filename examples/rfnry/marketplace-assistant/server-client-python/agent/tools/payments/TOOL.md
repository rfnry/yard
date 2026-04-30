---
name: Payments
description: Payment record by id. Returns method, status (authorized|captured), and amount.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8202/payments/{input.payment_id}
  timeout: 10
input:
  payment_id:
    type: string
    description: Payment id in the form MKT-PAY-NNNNN.
    required: true
---
