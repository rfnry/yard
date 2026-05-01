from __future__ import annotations

from pydantic import BaseModel, Field


class Source(BaseModel):
    tool: str
    detail: str


class Headline(BaseModel):
    date: str
    source: str
    text: str


class MarketScan(BaseModel):
    ticker: str
    ticker_in_coverage: bool
    summary: str
    price_commentary: str | None = None
    headlines: list[Headline] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)


class CompetitorProfile(BaseModel):
    ticker: str
    name: str | None = None
    sector: str | None = None
    founded: int | None = None
    hq: str | None = None
    price: float | None = None
    market_cap_usd: int | None = None
    pe_ratio: float | None = None
    ytd_change_pct: float | None = None
    headlines: list[Headline] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)


class WeeklyTickerLine(BaseModel):
    ticker: str
    price: float | None = None
    ytd_change_pct: float | None = None
    notable_headline: str | None = None


class WeeklySummary(BaseModel):
    tickers: list[WeeklyTickerLine] = Field(default_factory=list)
    biggest_mover: str | None = None
    notes: str = ""
    sources: list[Source] = Field(default_factory=list)
