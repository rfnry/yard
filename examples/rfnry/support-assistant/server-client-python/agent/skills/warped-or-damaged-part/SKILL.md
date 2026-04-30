---
name: warped-or-damaged-part
trigger: customer reports the part arrived warped, broken, missing, or otherwise visibly defective on receipt
---

# Warped or Damaged Part

Pre-delivery damage flow.

1. Call `Order` with the order id from the rep's message.
   - If 404, surface it under **Findings** and stop. Don't continue
     this skill.
2. Call `Catalog` with the part id from the order — confirm part name,
   warranty months, price.
3. Call `Shipping` with the order's `tracking_id` — note carrier and
   delivery status.
4. Call `Customer` with `order.customer_id` — note tier
   (`trade_account` vs `consumer`); trade accounts get account-credit
   options that consumers don't (flag under **Open questions** if
   relevant).
5. Apply `knowledge/replacement.md` — pre-delivery damage = immediate
   replacement, no return required.
6. Apply `knowledge/expedited-shipping.md` — if the part is safety
   critical or the rep noted supervisor approval, expedited is free.

In **Recommendation**, name the customer-facing message the rep
should send, in plain prose. Do not invent a return address or RMA
number; tell the rep to "use the standard photo-evidence email
address" instead.
