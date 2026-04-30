---
name: credibility-cross-check
trigger: lawyer asks whether a stated fact (employer, business ownership, address) matches the registry
---

# Credibility Cross-Check

The lawyer says something like: "The witness claims they've worked
at Northbridge Holdings since 2017 — verify."

1. Identify the asserted fact and the relevant tool:
   - Employer claim → `EmploymentHistory(person_id)`
   - Business-ownership claim → `BusinessRegistry(business_id)`
   - Address claim → `Identity` or `PropertyRecords`
2. Call that tool.
3. Compare the claim to the result and report **only** what matches
   and what doesn't. Don't infer motive ("the discrepancy suggests
   …"). The lawyer infers; you report.

Example **Summary**:

> EmploymentHistory for ID-1024 lists Northbridge Holdings LLC
> beginning 2017-08, role "managing partner". The claim ("since
> 2017") matches; the role ("partner") aligns. No discrepancy
> surfaced.
