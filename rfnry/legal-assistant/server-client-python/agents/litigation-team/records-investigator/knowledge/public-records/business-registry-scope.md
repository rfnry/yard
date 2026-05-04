# Business Registry Scope

`BusinessRegistry` covers entity formation filings:

- LLCs, corporations, LPs, LLPs, trusts (where filed), nonprofits
- registered agents, principals (where the filing requires them)
- formation date, status (active / dissolved / forfeited)
- foreign-entity filings (an entity formed in DE but registered to
  do business in NY appears once per state)

Critical gaps:

- **Beneficial ownership is not always disclosed.** Many states
  require only the registered agent + organizer, not the actual
  owners. `principals: unavailable` is common and meaningful.
- **Trusts that don't wrap an LLC** typically aren't here.
- **Sole proprietorships** aren't entities — they don't appear at
  all.

Dissolved entities remain queryable. Status field disambiguates.
