---
name: CatalogSearch
description: Search the catalog by free-text query (matches part name or model compatibility). Returns a list of catalog entries.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8201/catalog?q={input.query}
  timeout: 10
input:
  query:
    type: string
    description: Free-text search term — typically a part name fragment or vehicle model.
    required: true
---
