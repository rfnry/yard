from __future__ import annotations

CATALOG = [
    {
        "sku": "ELEC-RTR-7800",
        "name": "MeshLink AX7800 Wi-Fi 6E Router",
        "category": "networking",
        "price_usd": 329.99,
        "msrp_usd": 379.99,
    },
    {
        "sku": "ELEC-LPT-X14",
        "name": "Apex X14 14\" Laptop (Ryzen 7, 16GB)",
        "category": "computers",
        "price_usd": 1199.0,
        "msrp_usd": 1349.0,
    },
    {
        "sku": "ELEC-HPH-Q30",
        "name": "Qubit Q30 Wireless Noise-Cancelling Headphones",
        "category": "audio",
        "price_usd": 248.5,
        "msrp_usd": 279.0,
    },
    {
        "sku": "ELEC-CAM-PRO5",
        "name": "Lumen Pro5 Mirrorless Camera Body",
        "category": "photography",
        "price_usd": 1799.0,
        "msrp_usd": 1899.0,
    },
    {
        "sku": "ELEC-MON-32U",
        "name": "Vista 32U 4K Studio Monitor",
        "category": "displays",
        "price_usd": 549.0,
        "msrp_usd": 649.0,
    },
]

STOCK_LEVELS = {
    "ELEC-RTR-7800": {"on_hand": 142, "reserved": 18, "reorder_at": 50, "warehouse": "atl-1"},
    "ELEC-LPT-X14": {"on_hand": 23, "reserved": 9, "reorder_at": 25, "warehouse": "atl-1"},
    "ELEC-HPH-Q30": {"on_hand": 411, "reserved": 47, "reorder_at": 100, "warehouse": "atl-1"},
    "ELEC-CAM-PRO5": {"on_hand": 7, "reserved": 4, "reorder_at": 10, "warehouse": "rno-2"},
    "ELEC-MON-32U": {"on_hand": 84, "reserved": 6, "reorder_at": 30, "warehouse": "atl-1"},
}

ORDERS = [
    {
        "order_id": "MKT-50001",
        "channel": "web",
        "skus": ["ELEC-RTR-7800"],
        "status": "shipped",
        "tracking_id": "MKT-TRK-50001",
        "payment_id": "MKT-PAY-50001",
        "total_usd": 329.99,
        "placed_at": "2026-04-22T13:11:00Z",
    },
    {
        "order_id": "MKT-50018",
        "channel": "amazon",
        "skus": ["ELEC-HPH-Q30", "ELEC-HPH-Q30"],
        "status": "processing",
        "tracking_id": None,
        "payment_id": "MKT-PAY-50018",
        "total_usd": 497.0,
        "placed_at": "2026-04-25T09:02:00Z",
    },
    {
        "order_id": "MKT-50033",
        "channel": "wholesale",
        "skus": ["ELEC-LPT-X14"] * 12,
        "status": "delivered",
        "tracking_id": "MKT-TRK-50033",
        "payment_id": "MKT-PAY-50033",
        "total_usd": 14_388.0,
        "placed_at": "2026-04-08T17:30:00Z",
    },
]

SHIPMENTS = [
    {
        "tracking_id": "MKT-TRK-50001",
        "carrier": "UPS",
        "status": "out_for_delivery",
        "last_scan_location": "Buyer city",
        "estimated_delivery_days": 0,
    },
    {
        "tracking_id": "MKT-TRK-50033",
        "carrier": "FedEx Freight",
        "status": "delivered",
        "last_scan_location": "Wholesale loading dock",
        "estimated_delivery_days": 0,
    },
]

PAYMENTS = [
    {
        "payment_id": "MKT-PAY-50001",
        "method": "stripe_card",
        "status": "captured",
        "amount_usd": 329.99,
    },
    {
        "payment_id": "MKT-PAY-50018",
        "method": "amazon_pay",
        "status": "authorized",
        "amount_usd": 497.0,
    },
    {
        "payment_id": "MKT-PAY-50033",
        "method": "net_30",
        "status": "captured",
        "amount_usd": 14_388.0,
    },
]

PROMOTIONS = [
    {
        "code": "WIFIWEEK",
        "discount_percent": 10,
        "applies_to_categories": ["networking"],
        "starts_at": "2026-04-20",
        "ends_at": "2026-04-30",
    },
    {
        "code": "AUDIODAYS",
        "discount_percent": 15,
        "applies_to_categories": ["audio"],
        "starts_at": "2026-04-25",
        "ends_at": "2026-05-05",
    },
]

SALES_SUMMARY = {
    "week": {
        "period": "week",
        "starts_at": "2026-04-21",
        "ends_at": "2026-04-27",
        "units_sold": 318,
        "revenue_usd": 84_211.45,
        "top_categories": ["networking", "audio", "computers"],
    },
    "month": {
        "period": "month",
        "starts_at": "2026-04-01",
        "ends_at": "2026-04-30",
        "units_sold": 1_402,
        "revenue_usd": 412_905.10,
        "top_categories": ["computers", "audio", "networking"],
    },
}
