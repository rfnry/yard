---
name: order-snapshot
trigger: user asks for an order with implied "and what's the status?" — i.e. anything beyond the order id alone
---

# Order Snapshot

1. Call `Order` with the order id — capture channel, skus, status,
   tracking_id, payment_id, total, placed_at.
2. If `tracking_id` is non-null, call `Shipping`.
3. Call `Payments` for the payment_id.
4. Render under `## <ORDER_ID>` with bullets:
   - status, total, channel, placed_at  (Order)
   - carrier, status, last_scan, eta_days  (Shipping) — or "no tracking yet"
   - method, status, amount  (Payments)
