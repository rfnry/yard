# Verdict strict mapping

| ConflictDatabase result | Verdict |
|---|---|
| `prior_representation: opposing` | `direct_conflict` |
| `prior_representation: aligned` | `clear` (note it though) |
| `no_record` | `clear` |
| HTTP error / timeout | `inconclusive` |

No other verdicts. No "soft conflict" or "watch for it." The
intake-coordinator decides downstream — your job is to map the DB
output to one of three values cleanly.
