# Categories

Five top-level categories. Each maps to the SKU `{CAT}` segment.

- **RTR (router):** consumer + small-business networking. Includes
  Wi-Fi 6/6E/7, mesh systems, PoE switches.
- **LAP (laptop):** business + consumer notebooks. Workstation-class
  desktops are not in this taxonomy — the firm doesn't sell them.
- **HDP (headphones):** over-ear, on-ear, in-ear, gaming headsets.
  Speakers and soundbars are **not** here; they're under DSP for
  legacy reasons.
- **CAM (camera):** mirrorless, DSLR, action, webcams. Drones used
  to be here; spun out into a separate catalog two years ago.
- **DSP (display):** monitors, TVs, projectors, soundbars. The
  soundbar grouping is historical — assume it stays that way.

Cross-category bundles (e.g. laptop + monitor) carry the `LAP` SKU
of the lead item; the bundle composition is in
`Catalog.bundle_items` when the field is non-null.
