from __future__ import annotations

from src.data import CATALOG_PARTS, CUSTOMERS, ORDERS, PAYMENTS, SHIPMENTS, fallback_part


def get_part(part_id: str) -> dict[str, object]:
    part_id_upper = part_id.upper()
    for entry in CATALOG_PARTS:
        if entry["part_id"] == part_id_upper:
            return entry
    return fallback_part(part_id_upper)


def search_catalog(query: str) -> list[dict[str, object]]:
    needle = query.strip().lower()
    if not needle:
        return CATALOG_PARTS
    return [
        part
        for part in CATALOG_PARTS
        if needle in str(part["name"]).lower()
        or any(needle in str(m).lower() for m in part["model_compatibility"])  # type: ignore[union-attr]
    ]


def get_order(order_id: str) -> dict[str, object] | None:
    for entry in ORDERS:
        if entry["order_id"] == order_id.upper():
            return entry
    return None


def list_orders_for_customer(customer_id: str) -> list[dict[str, object]]:
    return [o for o in ORDERS if o["customer_id"] == customer_id.upper()]


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


def get_customer(customer_id: str) -> dict[str, object] | None:
    for entry in CUSTOMERS:
        if entry["customer_id"] == customer_id.upper():
            return entry
    return None
