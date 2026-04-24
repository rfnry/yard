---
name: triage
description: Classify a ticket and suggest the next step. Refining frames which policy applies; critic grades whether escalation was recommended when required.
refining:
  level: 2
---

# Triage

Input: a ticket summary.
Output: `action` (refund | replace | escalate | info) + policy citation + one-line rationale.

Refining surfaces prior similar tickets; critic checks that safety/legal/accessibility cases escalated.
