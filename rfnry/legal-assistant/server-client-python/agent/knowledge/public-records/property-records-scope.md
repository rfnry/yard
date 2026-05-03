# Property Records Scope

`PropertyRecords` returns deed + tax-roll data:

- owner of record (legal entity or natural person)
- assessed value (latest tax year)
- transaction history (sale price, date, prior owner) for the last
  20 years where on file
- tenant occupancy flag (yes/no/unknown — derived from tax mailing
  address vs. property address)

Coverage is **county-level**, with full coverage in 2,800 of ~3,100
US counties. Rural counties more often return "tax-roll only — no
deed text on file".

Trust-held property quirk: when the owner of record is a trust, the
trust name appears (e.g. "Northbridge Family Trust"). To resolve
who controls the trust, cross-reference with `BusinessRegistry`
(many trusts are filed there, especially LLC-wrapped ones). If the
trust is unregistered, this source has no way to look through it —
report "owner: trust; settlor unknown from public records".
