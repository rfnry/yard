# Retention

Pulled records are retained for the life of the case plus 7 years.
Storage is per-`case_id` under the firm's archival store; this
assistant has no role in archival — its session events and reports
are the working trail, not the canonical record.

When a case closes, the lead attorney triggers an archive job that
sweeps the case's working files into long-term storage. After
archive, the live data folder for that `case_id` is wiped.

Investigative reports produced here are **drafts**. The canonical
report is the one the attorney signs and files. Don't represent the
output of this tool as a finished work product.
