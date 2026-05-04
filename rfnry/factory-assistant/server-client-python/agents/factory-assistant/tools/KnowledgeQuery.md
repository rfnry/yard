---
name: KnowledgeQuery
description: Search the indexed factory documentation (manuals, mechanical drawings, meeting transcripts) and return the most relevant passages with source ids and grounding metadata. Always call this before answering — never answer from prior-turn memory of an earlier query.
executor: python
config:
  function: knowledge_query
input:
  query:
    type: string
    description: The technician's question, or a sharpened reformulation of it. Quote fault codes and machine names verbatim — fault tables are indexed strictly.
    required: true
  knowledge_id:
    type: string
    description: Optional knowledge slice override. Defaults to the configured factory corpus. Use a separate slice id only when ingestion routed documents into one.
    required: false
---
