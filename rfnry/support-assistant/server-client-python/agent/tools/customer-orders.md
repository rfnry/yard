---
name: CustomerOrders
description: List the orders associated with a single customer id. Returns an array of order summaries.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8201/orders/by-customer/{input.customer_id}
  timeout: 10
input:
  customer_id:
    type: string
    description: Customer id in the form CUST-NNNN.
    required: true
---
