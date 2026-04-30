# Tools

- **Catalog** — Look up a product by SKU. Returns name, category, price, and msrp.
- **CatalogSearch** — Search the catalog by free-text query and optional category filter. Returns a list of products.
- **Order** — Look up an order by id. Returns channel (web|amazon|wholesale), skus, status, tracking_id, payment_id, total, placed_at.
- **Payments** — Payment record by id. Returns method, status (authorized|captured), and amount.
- **Promotions** — List currently active promotion codes with their discount percent and applicable categories.
- **RecentOrders** — Recent orders within the last N days. Returns a list of order summaries.
- **SalesSummary** — Aggregate sales for a period. Returns units_sold, revenue_usd, and top_categories.
- **Shipping** — Tracking status by tracking id. Returns carrier, status, last_scan_location, estimated_delivery_days.
- **Stock** — Current inventory for a SKU. Returns on_hand, reserved, available, reorder_at, below_reorder flag, and warehouse.
