---
name: maintenance-step
trigger: technician asks for a single step or check in a planned maintenance procedure ("what torque on the platen bolts", "what's the target nitrogen pre-charge", "which filter goes in F-411")
---

# Maintenance Step

1. Call `KnowledgeQuery` with the part or procedure name plus the
   datum the technician is asking for ("HP-1200 platen mounting
   bolts torque", "A-203 nitrogen pre-charge target", "F-411
   cartridge part number").
2. Pick the most specific source. Manuals beat transcripts for
   maintenance numbers; transcripts beat manuals only when the
   transcript explicitly supersedes the manual ("we revised this
   number after the 2026-04 incident").
3. Reply:
   - **Answer** is short — one sentence with the number/part/step.
   - **Source** quotes the exact phrasing from the manual or
     drawing, with section number and page where available.
4. If the technician asks for a value the source gives as a range
   ("180 to 220 bar"), give the range, not the midpoint.

A common failure mode here is to confidently return a value from a
similar machine in the corpus. Don't. If the technician asks about
the HP-1200 and the corpus only has the HP-1500, say so under
**What I could not find** and stop.
