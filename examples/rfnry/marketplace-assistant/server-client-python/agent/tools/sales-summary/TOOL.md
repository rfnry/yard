---
name: SalesSummary
description: Aggregate sales for a period. Returns units_sold, revenue_usd, and top_categories.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8200/marketplace-assistant/sales-summary?period={input.period}
  timeout: 10
input:
  period:
    type: string
    description: Period name — "week" or "month".
    required: true
---
