# Chain of Custody

The mock public-records sources behind this assistant return data
with the following provenance fields:

- `as_of` — when the source last refreshed the underlying record
- `source_system` — the upstream system (e.g. PACER, county
  recorder, Sec. of State)
- `vendor_id` — the data vendor that aggregated the source

These three fields, plus the tool call's timestamp, are sufficient
for an investigator to retrace the lookup. They are **not**
sufficient to authenticate the record at trial — for that, the
firm pulls a certified copy from the source system directly.

When a lookup returns a record that may end up offered as evidence,
flag the `Followups` section: "request certified copy from
{source_system}".
