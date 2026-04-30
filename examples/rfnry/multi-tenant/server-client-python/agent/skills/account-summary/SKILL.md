---
name: account-summary
trigger: user asks "what's in my account?", "show me my data", or similar
---

# Account Summary

When the user asks for an overview of their account:

1. Read the active scope's `MEMORY.md` if it exists (your `Read` tool
   resolves it within the path-jail; you do not need to know the
   absolute path).
2. Summarize the contents in 3–5 bullet points: most recent session,
   any open issues noted in memory, last action taken.
3. If `MEMORY.md` is empty or missing, say: "Your account is fresh —
   no prior sessions on file."
4. Never include any data not loaded from the active scope.
