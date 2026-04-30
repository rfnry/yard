---
name: Promotions
description: List currently active promotion codes with their discount percent and applicable categories.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8202/promotions
  timeout: 10
input: {}
---
