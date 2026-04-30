from __future__ import annotations

import hashlib

CATALOG_PARTS = [
    {
        "part_id": "PART-12345",
        "name": "Brake Caliper - Front Right",
        "model_compatibility": ["Civic 2018-2022", "Accord 2019-2023"],
        "price_usd": 142.5,
        "warranty_months": 24,
    },
    {
        "part_id": "PART-22871",
        "name": "Timing Belt Kit",
        "model_compatibility": ["Camry 2017-2021"],
        "price_usd": 89.0,
        "warranty_months": 36,
    },
    {
        "part_id": "PART-44102",
        "name": "Oxygen Sensor (Bank 1)",
        "model_compatibility": ["F-150 2015-2020", "Mustang 2018-2022"],
        "price_usd": 64.75,
        "warranty_months": 12,
    },
    {
        "part_id": "PART-55230",
        "name": "Strut Assembly - Rear",
        "model_compatibility": ["RAV4 2016-2020"],
        "price_usd": 215.0,
        "warranty_months": 24,
    },
]

ORDERS = [
    {
        "order_id": "ORD-100045",
        "customer_id": "CUST-7711",
        "part_ids": ["PART-12345"],
        "status": "shipped",
        "tracking_id": "TRK-AAA-0045",
        "payment_id": "PAY-100045",
        "total_usd": 142.5,
    },
    {
        "order_id": "ORD-100092",
        "customer_id": "CUST-8801",
        "part_ids": ["PART-22871", "PART-44102"],
        "status": "processing",
        "tracking_id": None,
        "payment_id": "PAY-100092",
        "total_usd": 153.75,
    },
    {
        "order_id": "ORD-100173",
        "customer_id": "CUST-7711",
        "part_ids": ["PART-55230", "PART-55230"],
        "status": "delivered",
        "tracking_id": "TRK-AAA-0173",
        "payment_id": "PAY-100173",
        "total_usd": 430.0,
    },
]

SHIPMENTS = [
    {
        "tracking_id": "TRK-AAA-0045",
        "carrier": "UPS",
        "status": "in_transit",
        "last_scan_location": "Memphis, TN",
        "estimated_delivery_days": 2,
    },
    {
        "tracking_id": "TRK-AAA-0173",
        "carrier": "FedEx",
        "status": "delivered",
        "last_scan_location": "Recipient address",
        "estimated_delivery_days": 0,
    },
]

PAYMENTS = [
    {
        "payment_id": "PAY-100045",
        "method": "credit_card_visa_4242",
        "status": "captured",
        "amount_usd": 142.5,
        "captured_at": "2026-04-21T10:14:00Z",
    },
    {
        "payment_id": "PAY-100092",
        "method": "credit_card_amex_1005",
        "status": "authorized",
        "amount_usd": 153.75,
        "captured_at": None,
    },
    {
        "payment_id": "PAY-100173",
        "method": "ach",
        "status": "captured",
        "amount_usd": 430.0,
        "captured_at": "2026-04-12T15:02:00Z",
    },
]

CUSTOMERS = [
    {
        "customer_id": "CUST-7711",
        "name": "Marcus Whitaker",
        "email": "marcus.whitaker@example.com",
        "tier": "trade_account",
        "lifetime_orders": 14,
    },
    {
        "customer_id": "CUST-8801",
        "name": "Petra Voss",
        "email": "petra.voss@example.com",
        "tier": "consumer",
        "lifetime_orders": 2,
    },
]


def fallback_part(part_id: str) -> dict[str, object]:
    digest = int(hashlib.sha256(part_id.encode()).hexdigest(), 16)
    return {
        "part_id": part_id,
        "name": f"Generic Part {part_id[-5:]}",
        "model_compatibility": [],
        "price_usd": round(20 + (digest % 500_00) / 100.0, 2),
        "warranty_months": 12,
        "_synthesized": True,
    }
