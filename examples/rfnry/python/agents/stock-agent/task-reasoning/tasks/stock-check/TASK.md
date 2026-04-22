---
name: stock-check
description: Look up a SKU and report stock level. Reflect before answering so past lookups inform phrasing.
reflection:
  level: 2
---

# Stock check

Input: a SKU, product name, or warehouse question.
Output: stock level + warehouse + one-line context.

The reflection pass consults past reflections for phrasing patterns; the critic grades whether the final answer cited the knowledge file.
