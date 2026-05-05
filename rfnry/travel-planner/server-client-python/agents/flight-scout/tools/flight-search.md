---
name: FlightSearch
description: Search round-trip flights between an origin/destination pair for a date range. Returns up to 10 ranked options.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8303/flights
  timeout: 15
input:
  origin:
    type: string
    description: Origin city or IATA airport code.
    required: true
  destination:
    type: string
    description: Destination city or IATA airport code.
    required: true
  depart_date:
    type: string
    description: Outbound date (ISO YYYY-MM-DD).
    required: true
  return_date:
    type: string
    description: Inbound date (ISO YYYY-MM-DD).
    required: true
  travelers:
    type: number
    description: Number of travelers.
    required: true
---

<!--
  RAG / API wiring stub.

  In a real deployment this would point at a flight aggregator
  (Amadeus, Skyscanner, Duffel, Kiwi, etc.) — the harness already
  gives us the HTTP executor + retry middleware + redaction. The
  rfnry side stays exactly as you see it: one declarative .md file
  declaring a tool the model can call. No Python required.
-->
