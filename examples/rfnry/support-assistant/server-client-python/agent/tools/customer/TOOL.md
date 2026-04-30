---
name: Customer
description: Look up a customer profile by customer id. Returns name, email, tier (trade_account|consumer), and lifetime order count.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8201/customers/{input.customer_id}
  timeout: 10
input:
  customer_id:
    type: string
    description: Customer id in the form CUST-NNNN.
    required: true
---
