---
name: Stock
description: Current inventory for a SKU. Returns on_hand, reserved, available, reorder_at, below_reorder flag, and warehouse.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8200/marketplace-assistant/stock/{input.sku}
  timeout: 10
input:
  sku:
    type: string
    description: SKU in the form ELEC-XXX-NNNN.
    required: true
---
