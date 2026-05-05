---
name: ActivitySearch
description: Search activities, tours, and experiences for a destination over a date range, biased to the requested mood.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8303/activities
  timeout: 15
input:
  destination:
    type: string
    description: Destination city or area.
    required: true
  start_date:
    type: string
    description: Trip start (ISO YYYY-MM-DD).
    required: true
  end_date:
    type: string
    description: Trip end (ISO YYYY-MM-DD).
    required: true
  travelers:
    type: number
    description: Number of travelers.
    required: true
  mood:
    type: string
    description: One of "relaxing" | "adventurous" | "cultural" | "family".
    required: false
---

<!--
  RAG / API wiring stub.

  Real deployment: Viator / GetYourGuide / Klook for tours, plus a
  city-guides RAG index for non-bookable suggestions (walks, parks,
  free museums). The mood field is what RAG over reviews would lean on.
-->
