from __future__ import annotations

from typing import Any

from src.data import COMPANIES, MARKET_SNAPSHOTS, NEWS


def get_company(ticker: str) -> dict[str, Any] | None:
    return COMPANIES.get(ticker.upper())


def get_market_snapshot(ticker: str) -> dict[str, Any] | None:
    snap = MARKET_SNAPSHOTS.get(ticker.upper())
    if snap is None:
        return None
    return {"ticker": ticker.upper(), **snap}


def get_news(ticker: str) -> list[dict[str, Any]]:
    return list(NEWS.get(ticker.upper(), []))


def list_companies() -> list[dict[str, Any]]:
    return [
        {"ticker": c["ticker"], "name": c["name"], "sector": c["sector"]}
        for c in COMPANIES.values()
    ]
