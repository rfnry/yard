# Warranty Policy

Each part ships with a warranty length set in the catalog:
`Catalog.warranty_months`. Some defaults to be aware of:

- **Brake calipers** — 24 months from delivery date.
- **Timing belts / chains** — 36 months from delivery date.
- **Sensors (oxygen, MAF, knock, etc.)** — 12 months from delivery
  date.
- **Strut / suspension assemblies** — 24 months from delivery date.

The authoritative number is whatever `Catalog.warranty_months`
returns for the specific `part_id`. Cite it in **Findings** as
`(Catalog PART-XXXXX warranty_months=24)`.

A claim is **in warranty** if:
`order.delivered_at + warranty_months > today`.

If the order never reached `delivered`, the warranty clock has not
started — the claim qualifies as a *pre-delivery defect*; see
`replacement.md`.
