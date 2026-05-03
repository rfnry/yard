---
name: company_profile
description: Profile of one covered company by ticker — name, sector, founded year, HQ city.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8204/companies/{input.ticker}
  timeout: 10
input:
  ticker:
    type: string
    description: Ticker symbol (e.g. AVNX, RPSE, MCLD).
    required: true
---
