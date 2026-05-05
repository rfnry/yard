---
name: plan-trip
input:
  origin:
    type: string
    required: true
  destination:
    type: string
    required: true
  arrival_date:
    type: string
    required: true
  departure_date:
    type: string
    required: true
  travelers:
    type: number
    required: true
  mood:
    type: string
    required: false
  budget_band:
    type: string
    required: false
steps:
  - name: scout
    parallel:
      - name: flights
        agent: flight-scout
        task: find-flights
        input: "Find round-trip flights {workflow.input.origin} to {workflow.input.destination}, depart {workflow.input.arrival_date}, return {workflow.input.departure_date}, {workflow.input.travelers} travelers."
      - name: hotels
        agent: hotel-scout
        task: find-hotels
        input: "Find lodging in {workflow.input.destination} from {workflow.input.arrival_date} to {workflow.input.departure_date} for {workflow.input.travelers} travelers (budget band: {workflow.input.budget_band})."
      - name: activities
        agent: activity-curator
        task: curate-activities
        input: "Curate activities in {workflow.input.destination} from {workflow.input.arrival_date} to {workflow.input.departure_date} for {workflow.input.travelers} travelers (mood: {workflow.input.mood})."
      - name: weather
        agent: weather-watcher
        task: forecast
        input: "Forecast weather in {workflow.input.destination} from {workflow.input.arrival_date} to {workflow.input.departure_date}."
  - name: synthesize
    agent: trip-synthesizer
    task: synthesize-trip
    input: "Compose one TripPlan from these four scout reports.\n\nFlights:\n{flights.output}\n\nHotels:\n{hotels.output}\n\nActivities:\n{activities.output}\n\nWeather:\n{weather.output}"
output: "{synthesize.output}"
---

# Plan Trip Workflow

The trip-planner workflow.

1. **scout** — runs four scouts **in parallel**: flights, hotels,
   activities, weather. Each is a fully-framed turn under its own
   task with its own per-task `output_schemas` enforcement. The four
   harness invocations run concurrently via `asyncio.gather`, so the
   wall-clock cost of the scout phase is the slowest single scout,
   not the sum.
2. **synthesize** — `trip-synthesizer` reads all four scout reports,
   picks one flight + one hotel, places activities on a calendar
   weighted by the weather advisories, and emits a single `TripPlan`.

Why this is a good fit for `parallel:`:

- The four scouts have **no cross-dependency** until the synthesis step.
- Each scout hits an **independent data source**, so latency is bound
  by the slowest API, not their sum.
- Failures are **isolated** — if `WeatherForecast` is down, the other
  three still complete; the synthesizer can degrade gracefully.

The workflow is registered with `OutputSchemas.workflows={"plan-trip":
TripPlan}` on the engine, so `engine.run_workflow(name="plan-trip",
expect=TripPlan)` returns a typed instance.
