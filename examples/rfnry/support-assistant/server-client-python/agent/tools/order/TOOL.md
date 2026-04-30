---
name: Order
description: Look up an order by order id. Returns customer id, part ids, status (processing|shipped|delivered), tracking id (if shipped), payment id, and total.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8201/orders/{input.order_id}
  timeout: 10
input:
  order_id:
    type: string
    description: Order id in the form ORD-NNNNNN.
    required: true
---
