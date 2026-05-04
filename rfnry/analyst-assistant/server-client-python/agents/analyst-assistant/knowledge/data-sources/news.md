# News

The `News` tool returns deduplicated wire and trade-publication
articles. Coverage:

- English-language wires (Reuters, Bloomberg, AP, Dow Jones)
- Major trade pubs by sector (industry-specific; not exhaustive)
- Press releases, dedup'd against the wire that picked them up

Lag is typically 5–15 minutes from publication; a near-real-time
news feed is **not** what this tool is. If the analyst needs
intraday breaking-news monitoring, that's outside the engagement's
data scope — flag it.

Dedup is by article body hash. If the same press release shows up
on three wires, you'll get one entry with `also_carried_by: [Reuters,
AP, Dow Jones]`. Quote the primary source, mention the carriers
when relevant for source diversity.
