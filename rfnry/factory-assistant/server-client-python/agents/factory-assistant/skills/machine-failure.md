---
name: machine-failure
trigger: technician describes a symptom without a fault code ("the platen is drifting", "there's a hissing sound from the manifold", "spindle won't reach speed")
---

# Machine Failure

1. Call `KnowledgeQuery` with the machine name plus the symptom
   verbatim ("HP-1200 platen drift during dwell", "MX-500 spindle
   slow to speed"). Quoting the technician's wording usually
   matches a manual's section heading.
2. If retrieval returns nothing, decompose:
   - Query the machine name alone to confirm it is in the corpus.
   - Query the symptom in plain language ("hydraulic chatter",
     "spindle overcurrent").
3. Cross-check whether the symptom shows up in a meeting transcript
   (an incident review can name the *real* root cause that the
   manual's diagnostic list buries near the bottom).
4. Reply:
   - **Answer** opens with what the technician should check first,
     based on the source's most-likely-cause ranking.
   - List the diagnostic steps in source order, verbatim.
   - If a transcript adds a recent caveat (e.g. "we've seen this
     specifically when the cooler bypass valve sticks"), include
     that under **Answer** and cite the transcript date.

If the source ranks causes by likelihood, preserve that ranking.
The technician needs to know which check is "try first" vs "try
last when nothing else worked".
