# Identity Coverage

The `Identity` source resolves a subject ID to:

- legal name (current + last two known aliases, when on file)
- DOB (year always; full date when available)
- current address (last verified, with verification date)
- `ssn_last4` (always; full SSN never returned)
- ID type (DL state + number, passport flag, ITIN flag)

Gaps:

- No phone numbers, email addresses, or social-media handles.
- Address history beyond the current verified address is not in
  `Identity` — use `PropertyRecords` for residence trail.
- ID-9999 onwards are synthetic test rows, not real subjects.

Refresh cadence: daily (verified addresses lag 24–48h behind the
underlying postal source).
