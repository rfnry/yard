from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src import services

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/catalog/{sku}")
async def get_product(sku: str) -> dict[str, object]:
    product = services.get_product(sku)
    if product is None:
        raise HTTPException(status_code=404, detail=f"sku not found: {sku}")
    return product


@router.get("/catalog")
async def search_catalog(q: str = "", category: str | None = None) -> dict[str, object]:
    return {"query": q, "category": category, "results": services.search_catalog(q, category)}


@router.get("/stock/{sku}")
async def get_stock(sku: str) -> dict[str, object]:
    level = services.get_stock(sku)
    if level is None:
        raise HTTPException(status_code=404, detail=f"sku not found in inventory: {sku}")
    return level


@router.get("/orders/{order_id}")
async def get_order(order_id: str) -> dict[str, object]:
    order = services.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail=f"order not found: {order_id}")
    return order


@router.get("/orders")
async def recent_orders(days: int = 30) -> dict[str, object]:
    return {"days": days, "orders": services.recent_orders(days)}


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


@router.get("/promotions")
async def active_promotions() -> dict[str, object]:
    return {"promotions": services.active_promotions()}


@router.get("/sales-summary")
async def sales_summary(period: str = "week") -> dict[str, object]:
    summary = services.sales_summary(period)
    if summary is None:
        raise HTTPException(status_code=404, detail=f"unknown period: {period} (try week|month)")
    return summary
