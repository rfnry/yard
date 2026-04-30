---
name: Payments
description: Look up a payment record by payment id. Returns payment method, status (authorized|captured|refunded), amount, and capture timestamp.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8200/support-assistant/payments/{input.payment_id}
  timeout: 10
input:
  payment_id:
    type: string
    description: Payment id in the form PAY-NNNNNN.
    required: true
---
