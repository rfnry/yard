# Promo Stacking

Active promos are returned by `Promotions.active`. Each carries a
`stack_class`:

- **`exclusive`** — does not stack with anything else, including
  volume tiers.
- **`category`** — stacks with other `category` promos but not
  with `exclusive` ones.
- **`shipping`** — stacks with anything; affects shipping cost
  only, not item price.
- **`tier`** — auto-applied volume tier; treated as a promo for
  reporting but doesn't stack with `exclusive` or `category`.

The `Promotions.compute_price` tool resolves all this for a given
SKU + buyer + quantity. Don't try to reproduce the math by hand —
quote what the tool returned and cite the promo IDs that applied.
