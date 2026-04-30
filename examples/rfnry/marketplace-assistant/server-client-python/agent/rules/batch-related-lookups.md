# Batch Related Lookups

When the user asks about a single SKU and the obvious adjacent
data is one tool call away, fetch it without being asked. Examples:

- Asked for **stock on a SKU** → also fetch `Catalog` for the same
  SKU (price, name, category make the stock number readable).
- Asked for **an order** → fetch `Shipping` (if there's a
  tracking_id) and `Payments`. The user almost always wants both.
- Asked for **active promotions** → no extra fetch needed.

Don't go further than that. Don't fetch every order for a customer
when only one was asked about. Don't pre-fetch sales summaries.
