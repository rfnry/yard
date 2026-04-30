---
name: RecentOrders
description: Recent orders within the last N days. Returns a list of order summaries.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8200/marketplace-assistant/orders?days={input.days}
  timeout: 10
input:
  days:
    type: integer
    description: Window in days (typically 7 or 30).
    required: true
---
