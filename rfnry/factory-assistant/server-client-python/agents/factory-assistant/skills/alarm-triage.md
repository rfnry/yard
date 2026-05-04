---
name: alarm-triage
trigger: technician reads a fault code or alarm banner from the HMI ("E-021 just popped", "we're getting H-104 on line 3")
---

# Alarm Triage

1. Call `KnowledgeQuery` with the fault code as written. If the
   technician gives the code in shorthand ("E21" for "E-021"),
   query both the shorthand and the formal form. Fault tables
   index strictly.
2. If the first query returns nothing, broaden: query the subsystem
   prefix (`E-0xx electrical`, `H-1xx hydraulic`) plus the symptom.
3. Identify whether the code is a **first-line recoverable** code
   (technician can clear within their time budget) or a
   **must-escalate** code. The fault-table reference card says so
   explicitly.
4. Reply:
   - **Answer** opens with the first concrete action (often
     "Stop the line" or "Clear the obstruction at <location>").
   - List the recovery steps verbatim from the source, in order.
     Do not condense them.
   - State the pass criterion the technician should look for after
     the recovery — also verbatim.
5. If the code matches an entry in the escalation rules, name the
   contact path under **Source**.

If two documents disagree on the recovery (e.g. the OEM manual says
one thing, the in-house quick-reference card says another), present
both and recommend the in-house card as authoritative for the
plant's variant. Surface the discrepancy under **What I could not
find**.
