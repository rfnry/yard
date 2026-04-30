---
name: refund-eligibility-check
trigger: customer asks for a refund or the rep asks "is this refundable?"
---

# Refund Eligibility Check

1. Call `Order` and `Payments` for the order id + payment id.
2. Confirm:
   - Order is within 30 days of delivery (per
     `knowledge/refund.md`).
   - Payment is `captured` (an `authorized` but uncaptured payment is
     just a void — different flow).
3. If eligible: full refund to the method on `Payments.method`.
   Note the processing window from `knowledge/refund.md`
   (card 5–7d, ACH 7–10d, wholesale = credit memo).
4. If the customer asked for a *partial* refund, do NOT recommend
   one. Flag under **Open questions** for supervisor review.
5. If outside the 30-day window or the part is used and not
   defective, refund is denied; recommend the rep redirect to the
   replacement-skill or escalate.
