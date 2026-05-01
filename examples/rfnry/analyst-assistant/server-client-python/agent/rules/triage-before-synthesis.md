# Triage before synthesis

Before pulling a snapshot or running a multi-ticker scan, confirm the
question is well-formed:

- Is the ticker in our coverage universe? (`/companies` lists it.)
- Does the request specify the right report shape? (scan vs. profile
  vs. weekly summary)

If the ticker isn't on file, say so and stop. Don't substitute a
"similar" company.
