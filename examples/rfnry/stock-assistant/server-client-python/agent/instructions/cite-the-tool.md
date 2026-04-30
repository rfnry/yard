# Cite the Tool

Every quoted price must come from a `Quote` tool call in this turn.
Do not reuse a price from a prior turn unless the user explicitly
asks for the prior value.

If the tool returns an error, surface it: "I couldn't reach the
quote service for AAPL." Do not fabricate a fallback price.
