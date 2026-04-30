# data-backend — support-assistant mock data

Standalone FastAPI server (port `8201`) serving deterministic mock
data for the support-assistant agent's HTTP tool calls. Lives next
to the agent server in this example dir; bundled into the same
`docker-compose.yml`.

## Endpoints

```
GET /catalog/{part_id}                  one part
GET /catalog?q=<text>                   search
GET /orders/{order_id}                  one order
GET /orders/by-customer/{customer_id}   list
GET /shipping/{tracking_id}             one shipment
GET /payments/{payment_id}              one payment
GET /customers/{customer_id}            one customer
GET /health
```

## Layout

```
src/
  main.py        FastAPI bootstrap
  routes.py      route handlers
  services.py    pure logic
  data.py        in-memory mock dataset
```

## Run

```bash
cd yard/examples/rfnry/support-assistant/data-backend
cp .env.example .env
uv sync --extra dev
uv run poe dev          # http://127.0.0.1:8201
```
