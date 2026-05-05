---
name: CourtForms
description: Required exhibits + form metadata for a filing kind in a given jurisdiction.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8203/court-forms/{input.jurisdiction}/{input.filing_kind}
  timeout: 10
input:
  jurisdiction:
    type: string
    description: Court jurisdiction (e.g. "S.D.N.Y." or "CA-Superior-LA").
    required: true
  filing_kind:
    type: string
    description: One of "motion-to-dismiss" | "complaint" | "brief" | "answer" | "discovery-request".
    required: true
---

<!--
  RAG / API wiring stub.

  Real deployment: PACER, Westlaw, Lexis, or in-house docket DB.
-->
