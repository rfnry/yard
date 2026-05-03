from __future__ import annotations

from src.data import (
    CATALOG,
    ORDERS,
    PAYMENTS,
    PROMOTIONS,
    SALES_SUMMARY,
    SHIPMENTS,
    STOCK_LEVELS,
)


def get_product(sku: str) -> dict[str, object] | None:
    sku_upper = sku.upper()
    for entry in CATALOG:
        if entry["sku"] == sku_upper:
            return entry
    return None


def search_catalog(query: str, category: str | None) -> list[dict[str, object]]:
    needle = query.strip().lower()
    cat = category.strip().lower() if category else None
    out: list[dict[str, object]] = []
    for entry in CATALOG:
        if cat is not None and str(entry["category"]).lower() != cat:
            continue
        if needle and needle not in str(entry["name"]).lower() and needle not in str(entry["sku"]).lower():
            continue
        out.append(entry)
    return out


def get_stock(sku: str) -> dict[str, object] | None:
    level = STOCK_LEVELS.get(sku.upper())
    if level is None:
        return None
    available = level["on_hand"] - level["reserved"]
    return {**level, "sku": sku.upper(), "available": available, "below_reorder": available < level["reorder_at"]}


def get_order(order_id: str) -> dict[str, object] | None:
    for entry in ORDERS:
        if entry["order_id"] == order_id.upper():
            return entry
    return None


def recent_orders(days: int) -> list[dict[str, object]]:
    cutoff_iso = "2026-04-01T00:00:00Z"
    if days <= 7:
        cutoff_iso = "2026-04-23T00:00:00Z"
    elif days <= 14:
        cutoff_iso = "2026-04-16T00:00:00Z"
    return [o for o in ORDERS if str(o["placed_at"]) >= cutoff_iso]


def get_shipment(tracking_id: str) -> dict[str, object] | None:
    for entry in SHIPMENTS:
        if entry["tracking_id"] == tracking_id.upper():
            return entry
    return None


def get_payment(payment_id: str) -> dict[str, object] | None:
    for entry in PAYMENTS:
        if entry["payment_id"] == payment_id.upper():
            return entry
    return None


def active_promotions() -> list[dict[str, object]]:
    return PROMOTIONS


def sales_summary(period: str) -> dict[str, object] | None:
    return SALES_SUMMARY.get(period.lower())
