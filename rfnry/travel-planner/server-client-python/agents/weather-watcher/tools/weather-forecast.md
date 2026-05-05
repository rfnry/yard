---
name: WeatherForecast
description: Daily weather forecast for a destination over a date range. Returns highs, lows, precip probability, and any advisories.
executor: http
config:
  method: GET
  url: http://127.0.0.1:8303/weather
  timeout: 10
input:
  destination:
    type: string
    description: Destination city or area.
    required: true
  start_date:
    type: string
    description: Forecast start (ISO YYYY-MM-DD).
    required: true
  end_date:
    type: string
    description: Forecast end (ISO YYYY-MM-DD).
    required: true
---

<!--
  RAG / API wiring stub.

  Real deployment: Open-Meteo, NOAA, or Tomorrow.io. Historical
  seasonal climatology RAG (over a typical-year index) would land
  next to this for trips planned far enough out that no live forecast
  reaches the date range.
-->
