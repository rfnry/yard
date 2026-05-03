# Wholesale Terms

Wholesale buyers get one of two payment terms, set on the customer
record (`Buyer.payment_terms`):

- **card** — charged at order time, ships when fulfilled.
- **net-30** — invoice issued at ship date; payment due 30 days
  after. Reserved for buyers with > 12 months of clean payment
  history.

Volume tiers (per SKU per order):

- 1–9 units: list price.
- 10–49 units: 8% off list.
- 50–99 units: 12% off list.
- 100+ units: 15% off list, plus account manager review.

The tiers do not stack with promotions — the buyer gets whichever
is larger, never both. (See `promo-stacking.md`.)
