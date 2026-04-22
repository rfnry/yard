---
name: triage
description: Classify a ticket and suggest the next step. Reflection frames which policy applies; critic grades whether escalation was recommended when required.
reflection:
  level: 2
---

# Triage

Input: a ticket summary.
Output: `action` (refund | replace | escalate | info) + policy citation + one-line rationale.

Reflection surfaces prior similar tickets; critic checks that safety/legal/accessibility cases escalated.
