---
name: Quote
description: Fetch the current stock quote for a ticker. Returns JSON with ticker, price, and currency.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8103/quote/{input.ticker}
  timeout: 10
input:
  ticker:
    type: string
    description: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL).
    required: true
---

# Quote

Calls the stub upstream at `/quote/{ticker}`. The upstream returns
deterministic JSON: `{"ticker":"AAPL","price":189.42,"currency":"USD","source":"stub"}`.

Pass the response back to the user verbatim — do not round, reword,
or paraphrase the price.
