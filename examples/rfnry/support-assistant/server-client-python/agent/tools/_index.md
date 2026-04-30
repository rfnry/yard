# Tools

- **Catalog** — Look up a single catalog part by part id. Returns part name, model compatibility, price, and warranty months.
- **CatalogSearch** — Search the catalog by free-text query (matches part name or model compatibility). Returns a list of catalog entries.
- **Customer** — Look up a customer profile by customer id. Returns name, email, tier (trade_account|consumer), and lifetime order count.
- **CustomerOrders** — List the orders associated with a single customer id. Returns an array of order summaries.
- **Order** — Look up an order by order id. Returns customer id, part ids, status (processing|shipped|delivered), tracking id (if shipped), payment id, and total.
- **Payments** — Look up a payment record by payment id. Returns payment method, status (authorized|captured|refunded), amount, and capture timestamp.
- **Shipping** — Look up shipping status by tracking id. Returns carrier, status, last scan location, and estimated delivery days.
