---
name: sku-snapshot
trigger: user asks for "the snapshot", "current state", or any combination of price/stock/promo for a single SKU
---

# SKU Snapshot

1. Call `Catalog` with the sku — capture name, category, price, msrp.
2. Call `Stock` with the sku — capture on_hand, reserved, available,
   reorder_at, below_reorder, warehouse.
3. Call `Promotions` — filter to entries whose
   `applies_to_categories` includes the sku's category.
4. Render a single section under `## <SKU>` with bullets for each
   relevant fact.

If `Catalog` returns 404, stop after step 1 and report the SKU as
not in catalog.
