---
name: market_snapshot
description: Current price, market cap, P/E ratio, and YTD change for one ticker. P/E may be null for unprofitable companies.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8204/market-snapshot/{input.ticker}
  timeout: 10
input:
  ticker:
    type: string
    description: Ticker symbol.
    required: true
---
