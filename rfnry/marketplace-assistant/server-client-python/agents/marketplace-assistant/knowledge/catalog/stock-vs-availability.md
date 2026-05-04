# Stock vs. Availability

Two fields, two meanings:

- `Stock.on_hand` — units physically in the warehouse right now.
- `Stock.available_to_ship` — units that aren't already allocated
  to open orders.

These differ when a large order has been placed but not yet
shipped — the units are still on the shelf (`on_hand` counts them)
but they are committed (`available_to_ship` does not).

When a salesperson asks "do we have it?", the honest answer is
`available_to_ship`. Surface both numbers when the difference is
large (>10%); a small gap is normal.

Backorder posture: `available_to_ship` can be negative when
preorders have been taken; this is a signal to flag, not to
silently round to zero.
