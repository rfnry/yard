---
name: CatalogSearch
description: Search the catalog by free-text query and optional category filter. Returns a list of products.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8202/catalog?q={input.query}
  timeout: 10
input:
  query:
    type: string
    description: Free-text search term — typically a product name or SKU fragment.
    required: true
---
