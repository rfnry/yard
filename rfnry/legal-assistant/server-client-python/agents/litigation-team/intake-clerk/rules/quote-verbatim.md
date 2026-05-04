# Quote Verbatim

Subject ids and asserted claims are copied from the lawyer's text
exactly, including capitalization and punctuation.

- The lawyer wrote `id-9876` (lowercase, hyphenated). Output
  `"subject_id": "id-9876"`. Do not normalize to `ID-9876`. If the
  format looks wrong to you, mention that under `notes` — do not
  silently fix it. The downstream agent depends on the lawyer's
  spelling.

- The lawyer wrote "she's been at Northbridge since 2017". Output
  `"specific_claims": ["she's been at Northbridge since 2017"]`. Do
  not rewrite to "subject claims employment at Northbridge Holdings
  beginning 2017". The verbatim phrasing is what the cross-check
  agent matches against the registry.

- The lawyer wrote "case OR-2014-CRM-04412". Output
  `"subject_id": "OR-2014-CRM-04412"`. Do not strip the `case` prefix
  unless it is part of the case-number format documented in the
  `case-pull` skill.

You are a classifier, not a normalizer. Normalization is the next
agent's job, and only if their skill explicitly says so.
