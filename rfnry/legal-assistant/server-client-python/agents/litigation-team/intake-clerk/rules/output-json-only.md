# Output JSON Only

Your reply is one fenced JSON block. The downstream workflow step
parses it; any prose around it breaks the parse and the workflow
fails noisily.

Do not include:

- "Here is the plan:" or any preamble.
- A trailing commentary ("Let me know if you want me to broaden the
  scope.").
- A markdown heading above the block.

Do include:

- The fenced block opening with three backticks and the language tag
  `json`.
- The JSON object on the lines between the fences.
- The closing fence on its own line.

If the request is genuinely unclassifiable (e.g. the lawyer asked
something that has nothing to do with public-records investigation),
return:

```json
{"subject_kind": "person", "subject_id": "", "skill": "witness-profile", "specific_claims": [], "notes": "request did not name a subject id"}
```

The downstream step will surface the empty subject_id as a failure
and the lawyer will be prompted to retry. That is the right
behavior — guessing is worse.
