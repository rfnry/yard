---
name: HotelSearch
description: Search hotels for a destination over a date range with a target party size. Returns up to 10 options with rating, recent-review summary, and total price.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8303/hotels
  timeout: 15
input:
  destination:
    type: string
    description: Destination city or area.
    required: true
  check_in:
    type: string
    description: Check-in date (ISO YYYY-MM-DD).
    required: true
  check_out:
    type: string
    description: Check-out date (ISO YYYY-MM-DD).
    required: true
  travelers:
    type: number
    description: Number of guests.
    required: true
  budget_band:
    type: string
    description: One of "budget" | "mid-range" | "premium". Defaults mid-range.
    required: false
---

<!--
  RAG / API wiring stub.

  Real deployment would hit Booking.com, Expedia, or a hotel-meta
  aggregator (RateHawk, HotelBeds). Recent-review summarization is the
  natural place to wire RAG over a reviews index keyed by hotel_id.
-->
