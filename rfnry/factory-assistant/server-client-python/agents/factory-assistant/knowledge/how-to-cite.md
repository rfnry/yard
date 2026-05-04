# How to Cite

The **Source** section lists every retrieved passage you used. One
bullet per fact, in the order they appear in **Answer**. The format:

```
- <source_id> · <section or page> — "<short verbatim quote anchoring the fact>"
```

Examples:

- `manual-cnc-mill-mx500.pdf` · §6.4 — "spindle drawbar pressure shall be 22 bar +/- 1 bar at idle"
- `drawing-mx500-spindle-cooling.pdf` · sheet 3 — "TS-401 mounted on coolant return line 200 mm downstream of port B1"
- `transcript-incident-2026-04-22.md` · 14:32 — "we narrowed it down to the bypass solenoid sticking, not the cooler itself"

The verbatim quote is the load-bearing part. A bare `source_id` line
is not a citation — the technician needs enough wording to find the
passage on the printed copy or in the binder.

If `KnowledgeQuery` returned a `score` for the passage, you do not
need to repeat it. The score informs your confidence in the answer;
the citation just shows your work.

When the retrieved passage came from a transcript, include the
timestamp or speaker tag if the corpus indexed it. Transcripts
are noisier than manuals, so showing the technician the exact
moment helps them weigh the source.
