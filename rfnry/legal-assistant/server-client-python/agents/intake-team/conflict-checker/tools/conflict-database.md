---
name: ConflictDatabase
description: Query the firm's conflict-of-interest database for a party id. Returns prior representation status (none, aligned, opposing).
executor: http
config:
  method: GET
  url: http://127.0.0.1:8203/conflicts/{input.party_id}
  timeout: 5
input:
  party_id:
    type: string
    description: Party id (ID-NNNN format, same shape as person ids).
    required: true
---

<!--
  RAG / API wiring stub.

  Real deployment: query against the firm's conflicts management system
  (Intapp Open, Aderant Compulaw, or an in-house DB). The data backend
  here is the same demo /conflicts route added to the legal-assistant's
  data-backend.
-->
