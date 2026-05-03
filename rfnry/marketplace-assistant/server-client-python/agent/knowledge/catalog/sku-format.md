# SKU Format

SKUs are `ELEC-{CAT}-{NNNN}` where:

- `ELEC` is the namespace (electronics retailer; legacy from when
  the firm also sold appliances under `APPL-...`)
- `{CAT}` is the three-letter category — `RTR` (router), `LAP`
  (laptop), `HDP` (headphones), `CAM` (camera), `DSP` (display)
- `{NNNN}` is a 4-digit sequence assigned at SKU creation; it has
  no semantic meaning (don't infer model year, tier, etc. from it)

Special cases:

- `-RB` suffix means refurbished (e.g. `ELEC-LAP-3340-RB`)
- `-EOL` suffix means end-of-life — still in catalog for warranty
  lookup but not orderable
