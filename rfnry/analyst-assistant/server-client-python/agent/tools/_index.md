# Tools

- **list_companies** — List every company in the coverage universe. Returns ticker, name, and sector for each. Use this first when the client asks about the sector at large or you don't know which tickers are on file.
- **company_profile** — Profile of one covered company by ticker — name, sector, founded year, HQ city.
- **market_snapshot** — Current price, market cap, P/E ratio, and YTD change for one ticker. P/E may be null for unprofitable companies.
- **news** — Recent news headlines for one ticker. Returns up to ten items with date, source, and headline. Empty list means no recent news on file (state that as a finding).
