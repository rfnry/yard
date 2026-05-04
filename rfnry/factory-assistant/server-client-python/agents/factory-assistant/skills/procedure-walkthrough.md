---
name: procedure-walkthrough
trigger: technician asks for a complete procedure ("walk me through the lockout sequence", "how do I calibrate PV-105", "what's the cooler plate-pack service")
---

# Procedure Walkthrough

1. Call `KnowledgeQuery` with the procedure name verbatim
   ("HP-1200 lockout sequence", "CAL-PV105", "cooler CL-401 plate
   pack service").
2. The retrieved passage will usually be a numbered list. Reproduce
   it **in full**, in the original order, with the original step
   numbering. A technician walking through a procedure does not
   want a "highlights" version.
3. If the procedure references another procedure as a prerequisite
   (e.g. "perform lockout sequence section 2.3 before opening any
   flange"), include that prerequisite as the first step of the
   reply and cite it.
4. Reply:
   - **Answer** opens with the safety preamble the source mandates
     (lockout, bleed pressure, isolate power), then the numbered
     steps verbatim.
   - **Source** cites the document and section number once;
     individual step citations are not needed because the steps are
     contiguous from one passage.
5. If the procedure document has a revision history at the top,
   note the current revision under **Source** so the technician can
   confirm they are looking at the same version on the printed copy
   on the wall.
