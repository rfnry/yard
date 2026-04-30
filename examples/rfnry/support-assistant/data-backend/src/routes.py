from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src import services

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/catalog/{part_id}")
async def get_part(part_id: str) -> dict[str, object]:
    return services.get_part(part_id)


@router.get("/catalog")
async def search_catalog(q: str = "") -> dict[str, object]:
    return {"query": q, "results": services.search_catalog(q)}


@router.get("/orders/{order_id}")
async def get_order(order_id: str) -> dict[str, object]:
    order = services.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail=f"order not found: {order_id}")
    return order


@router.get("/orders/by-customer/{customer_id}")
async def list_orders_for_customer(customer_id: str) -> dict[str, object]:
    return {
        "customer_id": customer_id.upper(),
        "orders": services.list_orders_for_customer(customer_id),
    }


@router.get("/shipping/{tracking_id}")
async def get_shipment(tracking_id: str) -> dict[str, object]:
    shipment = services.get_shipment(tracking_id)
    if shipment is None:
        raise HTTPException(status_code=404, detail=f"tracking not found: {tracking_id}")
    return shipment


@router.get("/payments/{payment_id}")
async def get_payment(payment_id: str) -> dict[str, object]:
    payment = services.get_payment(payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail=f"payment not found: {payment_id}")
    return payment


@router.get("/customers/{customer_id}")
async def get_customer(customer_id: str) -> dict[str, object]:
    customer = services.get_customer(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail=f"customer not found: {customer_id}")
    return customer
