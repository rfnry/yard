---
name: news
description: Recent news headlines for one ticker. Returns up to ten items with date, source, and headline. Empty list means no recent news on file (state that as a finding).
executor: http
config:
  method: GET
  url: http://127.0.0.1:8204/news/{input.ticker}
  timeout: 10
input:
  ticker:
    type: string
    description: Ticker symbol.
    required: true
---
