---
name: classify-request
---

# Classify Request

The primary task: read a free-form lawyer request and produce one
fenced JSON block matching the schema in `AGENT.md`.

A good outcome:

- The JSON parses on the first try (downstream consumer is strict).
- `subject_kind` matches the named subject's id format.
- `skill` matches the lawyer's intent (full sweep / cross-check /
  case pull).
- `specific_claims` quotes the lawyer verbatim.
- `notes` is empty unless something genuinely needs flagging
  (multiple subjects, malformed id, ambiguous skill).

A bad outcome:

- Any text outside the fenced block.
- Normalized ids that change the lawyer's spelling.
- Paraphrased claims.
- Invented new skill names.
- Filling `notes` with chatter ("ready for downstream", "please
  proceed") instead of leaving it empty.
