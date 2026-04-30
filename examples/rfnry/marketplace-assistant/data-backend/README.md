# data-backend — marketplace-assistant mock data

Standalone FastAPI server (port `8202`) serving deterministic mock
data for the marketplace-assistant agent's HTTP tool calls.

## Endpoints

```
GET /catalog/{sku}              one product
GET /catalog?q=<text>           search
GET /stock/{sku}                one inventory snapshot
GET /orders/{order_id}          one order
GET /orders?days=<n>            recent orders
GET /shipping/{tracking_id}     one shipment
GET /payments/{payment_id}      one payment
GET /promotions                 active promotions
GET /sales-summary?period=…     week | month rollup
GET /health
```

## Run

```bash
cd yard/examples/rfnry/marketplace-assistant/data-backend
cp .env.example .env
uv sync --extra dev
uv run poe dev          # http://127.0.0.1:8202
```
