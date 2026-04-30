---
name: Catalog
description: Look up a product by SKU. Returns name, category, price, and msrp.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8200/marketplace-assistant/catalog/{input.sku}
  timeout: 10
input:
  sku:
    type: string
    description: SKU in the form ELEC-XXX-NNNN (e.g. ELEC-RTR-7800).
    required: true
---
