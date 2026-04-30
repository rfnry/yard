---
name: Catalog
description: Look up a single catalog part by part id. Returns part name, model compatibility, price, and warranty months.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8201/catalog/{input.part_id}
  timeout: 10
input:
  part_id:
    type: string
    description: Part identifier in the form PART-XXXXX (5+ digits).
    required: true
---
