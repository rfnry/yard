---
name: StatuteLookup
description: Look up a cited statute by its citation string. Returns whether the statute is current, repealed, or never existed.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8203/statutes
  timeout: 10
input:
  citation:
    type: string
    description: Citation string (e.g. "Fed. R. Civ. P. 12(b)(6)").
    required: true
---

<!--
  RAG / API wiring stub.

  Real deployment: Westlaw KeyCite / Lexis Shepard's, or an in-house
  citator. RAG over an annotated-statutes corpus would land here for
  the "is this statute applicable to the facts" question.
-->
