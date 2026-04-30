---
name: in-warranty-defect
trigger: customer reports a defect that surfaced after the part was installed and used
---

# In-Warranty Defect

1. Call `Order` for the order id; capture `delivered_at` and
   `customer_id`.
2. Call `Catalog` for the part id; capture `warranty_months`.
3. Compute warranty status (per `knowledge/warranty.md`):
   `delivered_at + warranty_months > today` → in warranty.
4. If in warranty AND under 90 days from delivery → ship replacement
   immediately, prepaid return label.
5. If in warranty AND over 90 days → customer returns first,
   replacement ships on receipt.
6. If out of warranty → no replacement; direct rep to refurbishment
   program (flag under **Open questions** that we don't have a
   refurb-program tool — rep handles externally).
7. Call `Customer` for tier; trade accounts may waive the return-
   first requirement (flag under **Open questions** if it's a
   `trade_account`).
