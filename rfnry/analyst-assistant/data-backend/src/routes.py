from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src import services

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/companies")
async def list_companies() -> dict[str, object]:
    return {"companies": services.list_companies()}


@router.get("/companies/{ticker}")
async def get_company(ticker: str) -> dict[str, object]:
    record = services.get_company(ticker)
    if record is None:
        raise HTTPException(status_code=404, detail=f"company not found: {ticker}")
    return record


@router.get("/market-snapshot/{ticker}")
async def get_market_snapshot(ticker: str) -> dict[str, object]:
    snap = services.get_market_snapshot(ticker)
    if snap is None:
        raise HTTPException(status_code=404, detail=f"snapshot not available: {ticker}")
    return snap


@router.get("/news/{ticker}")
async def get_news(ticker: str) -> dict[str, object]:
    return {"ticker": ticker.upper(), "items": services.get_news(ticker)}
