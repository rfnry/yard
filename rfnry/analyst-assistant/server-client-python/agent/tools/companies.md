---
name: list_companies
description: List every company in the coverage universe. Returns ticker, name, and sector for each. Use this first when the client asks about the sector at large or you don't know which tickers are on file.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8204/companies
  timeout: 10
input: {}
---
