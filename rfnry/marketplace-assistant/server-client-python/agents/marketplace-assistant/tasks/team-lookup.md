---
name: team-lookup
---

# Team Lookup

The primary task: a Sales or Marketing team member asks about the
current state of one or more SKUs, orders, promos, or sales rollups.

A good outcome:

- Every fact in the reply came from a tool call this turn.
- The shape is one `## <topic>` section per requested thing,
  bulleted facts inside.
- No unsolicited recommendations, opinions, or trend claims.
- The right skill fired when the user asked for a snapshot, an
  order picture, or a weekly pulse.

A bad outcome:

- Hallucinated SKUs, prices, or stock numbers.
- "Up from last week" or other comparisons without a tool call to
  back them.
- Long prose response with the data buried.
- Missed the obvious adjacent fetch (stock without catalog,
  order without shipping/payment).
