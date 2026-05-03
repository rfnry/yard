# Returns

Return window depends on channel — read `Order.channel`:

- **retail (DTC):** 30 days from delivery, no questions asked
  unless the unit is damaged on receipt back.
- **wholesale:** 14 days from ship date, only for defects or
  shortage. No buyer's-remorse returns.
- **refurb (`-RB` SKUs):** 14 days from delivery, defects only.
- **end-of-life (`-EOL` SKUs):** no returns; warranty replacement
  only via the manufacturer.

The window is a hard fact from the order date — don't compute it
loosely. The `Order.return_eligible_until` field has the exact
cutoff.
