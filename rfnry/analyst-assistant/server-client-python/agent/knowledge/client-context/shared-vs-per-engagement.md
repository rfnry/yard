# Shared vs. Per-Engagement Knowledge

The agent serves many clients. Each `client_id` is its own
engagement with its own retainer and research priorities. Two
shapes of knowledge:

- **Shared** — the things in `data-sources/`, `methodology/`,
  `client-context/`. These apply to every engagement: how the
  tools work, how citations are formed, what a peer comparison
  means.

- **Per-engagement** — the priority lists, peer sets, custom
  watchlists, sector-specific definitions a particular client cares
  about. These land at the **top level** of `knowledge/` (e.g.
  `knowledge/acme-corp-priorities.md`) when an analyst onboards a
  client, and the top-level `_index.md` should list them.

The reason for the split: the model loads `_index.md` at boot for
every turn under every `client_id`. Shared content is referenced
by drilling into a subdirectory; per-engagement content is listed
at the top level so the lead analyst sees it on the first page of
the index.

Do not put one client's notes inside `data-sources/` or
`methodology/` — the cross-client pollution would mean a turn for
client A has client B's notes one Read away. The path jail does
not help here because the model is allowed to read all of
`knowledge/`; the discipline is editorial.
