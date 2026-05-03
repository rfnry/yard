# Criminal Records Scope

`CriminalRecords` covers convictions and dispositions across federal
and state systems with the following caveats:

- **Federal:** complete back to 1990. PACER-derived; sealed dockets
  return as "sealed: yes" with no further detail.
- **State:** 47 states. Missing: HI, MA, WY (no agreement with the
  source provider). For these states, return "state coverage:
  unavailable" alongside any federal results.
- **Juvenile:** never returned, regardless of state — this source
  redacts juvenile entries upstream.
- **Expungements:** when a record is expunged, the source returns
  "expunged: yes" with the original charge redacted. The fact of
  expungement is itself reportable; the underlying charge is not.

Sentences are returned as tuples of (length, suspended, served). Do
not summarize "served 2 years" if the tuple says (2y, 1y, 1y) —
quote the structure.
