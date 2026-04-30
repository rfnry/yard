---
name: order-status-lookup
trigger: customer asks "where's my order?" or the rep needs an order summary
---

# Order Status Lookup

1. Call `Order` with the order id.
   - If the rep gave a customer id but no order id, call
     `CustomerOrders` instead and pick the most recent order.
2. If the order has a `tracking_id`, call `Shipping`. If not, the
   order is still pre-shipment; status is `processing` and there's
   no carrier data yet.
3. Report under **Findings**:
   - Order status (`Order.status`)
   - Carrier + last scan + ETA (`Shipping.*`)
   - Total + payment state (`Payments.status`)
4. **Recommendation** is short: a one-line "the customer should
   expect …" the rep can paste.
