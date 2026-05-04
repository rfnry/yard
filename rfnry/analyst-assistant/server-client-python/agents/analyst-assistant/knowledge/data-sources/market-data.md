# Market Data

`MarketData` returns daily OHLCV per ticker by default. Tick-level
data is available via `granularity: "tick"` but the engagement
needs to allow it (cost-controlled).

Corporate actions (splits, dividends, mergers) are applied to the
back-history when you query — the returned series is
adjusted-close. If you need raw close, pass `adjust: false` and
note which actions were applied separately.

Coverage:

- US equities: complete back to 1990
- Major non-US listings (LSE, TSE, Euronext, HKEX): back to 2000
- ETFs, REITs: same dates as their primary listing

Currency: prices are in the listing's native currency. Don't
silently convert to USD; if the user asked for USD, do the
conversion explicitly and cite the FX rate + date.
