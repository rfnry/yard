# Missing Data Is a Finding

When a tool returns nothing for a query that should have hit
something, the absence is the finding. Don't paper over it.

Examples:

- "No 8-K filings in the 90 days following the announcement"
  (Filings, search type=8-K, date range, ticker). This may itself
  be the lead the analyst was looking for.
- "No press coverage of the executive change beyond the issuer's
  own release" (News, search "{name} appointed", date range).
- "No 13F holdings reported by {fund} for {ticker} as of latest
  quarter" (Filings, 13F, fund, FYxx Qy).

The shape of the negative finding is the same as a positive one:
cite the tool + the discriminating field. The reader should know
exactly what was searched and what came back empty.
