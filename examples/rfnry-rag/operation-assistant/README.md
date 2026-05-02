# operation-assistant

A factory-operations RAG service: ingest **manuals** (textual PDFs) and
**mechanical drawings** (vision-extracted PDFs) into one knowledge source,
then answer technician questions about machines, components, and wiring.

## Layout

```
operation-assistant/
├── docker-compose.yml      # qdrant + postgres + neo4j
├── documents/              # source markdowns + generated PDFs + the renderer
│   ├── md_to_pdf.py        # uv-runnable PEP 723 script
│   ├── *.md                # write your fixtures here
│   └── *.pdf               # rendered output (committed)
└── python/                 # the server, this language's example
    ├── pyproject.toml
    └── src/
        ├── main.py         # FastAPI entrypoint (infra only)
        ├── rag.py          # RagEngine factory + lifespan
        ├── routes.py       # /ingest, /query, /knowledge, /sources/{id}, /health
        └── schemas.py
```

Future examples (TypeScript, Go, …) live alongside `python/` under their own
sub-directories.

## How it works

One `KNOWLEDGE_ID` (default: `machines`) holds everything. Per ingest:

| `source_type` | Pipeline                                                              |
|---------------|-----------------------------------------------------------------------|
| `manual`      | text parser → chunk → vector + BM25 + Postgres FTS, parent-child on   |
| `drawing`     | vision LLM (Anthropic) → component/connection extraction → vector + graph edges (Neo4j) |

At query time, multi-path retrieval (vector + document + graph) fuses with RRF.
`QueryMode.AUTO` routes per-query: corpora under `FULL_CONTEXT_THRESHOLD` skip
retrieval and ride the prompt-cached prefix; larger corpora go through the
indexed pipeline. Grounding gate is on with `threshold=0.4`.

## Run

```bash
cd yard/examples/rfnry-rag/operation-assistant

docker compose up -d                       # qdrant + postgres + neo4j

cd python
cp .env.example .env                       # fill OPENAI_API_KEY + ANTHROPIC_API_KEY
uv sync --extra dev
uv run poe dev                             # http://0.0.0.0:8201
```

## Fixtures

`documents/md_to_pdf.py` is a self-contained uv script (PEP 723); it has no
ties to the server's environment.

```bash
# from the repo root or anywhere
uv run yard/examples/rfnry-rag/operation-assistant/documents/md_to_pdf.py
```

That renders every `*.md` in `documents/` to a sibling `*.pdf`. Drop more
markdown files in there and re-run. The PDFs are committed alongside their
markdown sources — no auto-ingestion, you upload them yourself.

## Driving an ingestion + query

The example does not auto-ingest. Use `/ingest` per file so you can exercise
the workflow end-to-end:

```bash
# manual
curl -X POST http://localhost:8201/ingest \
  -F 'file=@../documents/manual-press-1200.pdf' \
  -F 'source_type=manual' \
  -F 'tags=press,hydraulic'

# drawing
curl -X POST http://localhost:8201/ingest \
  -F 'file=@../documents/drawing-cl-401-cooler-loop.pdf' \
  -F 'source_type=drawing'

# ask
curl -X POST http://localhost:8201/query \
  -H 'content-type: application/json' \
  -d '{"query":"the platen of the HP-1200 drifts during dwell, what should I check?"}'

# inspect
curl http://localhost:8201/knowledge

# remove
curl -X DELETE http://localhost:8201/sources/<source_id>
```

### Demonstrating AUTO routing to FULL_CONTEXT

The first two docs (`manual-press-1200.pdf` and `drawing-cl-401-cooler-loop.pdf`)
share the default `KNOWLEDGE_ID=machines` and exercise the **INDEXED** pipeline
(vector + BM25 + FTS + graph fused with RRF).

The third doc, `fault-code-lookup.pdf`, is a small self-contained reference card.
Ingest it under a **separate** `knowledge_id` so its corpus stays well below
`FULL_CONTEXT_THRESHOLD` (150k tokens). When you query that knowledge_id with
`QueryMode.AUTO`, the engine skips retrieval and loads the whole corpus into the
prompt — the **FULL_CONTEXT** path:

```bash
# ingest into its own small knowledge slice
curl -X POST http://localhost:8201/ingest \
  -F 'file=@../documents/fault-code-lookup.pdf' \
  -F 'source_type=manual' \
  -F 'knowledge_id=quick-reference' \
  -F 'tags=fault-codes,reference'

# query that knowledge_id — AUTO will route to FULL_CONTEXT
curl -X POST http://localhost:8201/query \
  -H 'content-type: application/json' \
  -d '{"knowledge_id":"quick-reference","query":"what should I do for an E-021 VFD overtemperature?"}'
```

The two knowledge_ids stay isolated: `machines` keeps demonstrating the indexed
pipeline; `quick-reference` keeps demonstrating the cached full-context path.

## Observability + telemetry

Both modules are wired and always-on:

- **Observability** uses `default_observability_sink()` — auto-detects: `PrettyStderrSink` when stderr is a TTY (developer terminals, color-tagged single-line records), `JsonlStderrSink` everywhere else (Docker, CI, log shippers). Override with `RFNRY_RAG_OBSERVABILITY_FORMAT={pretty,json}`; honors `NO_COLOR`.
- **Telemetry** auto-wires `SqlAlchemyTelemetrySink(metadata_store)` whenever `RagEngineConfig` receives a `metadata_store` and no explicit telemetry sink — one row per query / ingest persists to the same Postgres database as metadata, in tables `rag_query_telemetry` and `rag_ingest_telemetry` (auto-created on init). Inspect rollups with the metadata store's URL:

```bash
psql "$POSTGRES_URL" -c "SELECT knowledge_id, COUNT(*) AS queries, SUM(tokens_input + tokens_output) AS total_tokens FROM rag_query_telemetry GROUP BY knowledge_id;"
psql "$POSTGRES_URL" -c "SELECT knowledge_id, source_id, outcome, duration_ms FROM rag_ingest_telemetry ORDER BY at DESC LIMIT 10;"
```

Pricing is downstream — the library emits raw token counts only. Apply rate cards in your admin UI / dashboard against `tokens_input`, `tokens_output`, `tokens_cache_creation`, `tokens_cache_read`.

## Tunables

`python/.env`:

| key                                | default                            | notes                                                                 |
|------------------------------------|------------------------------------|-----------------------------------------------------------------------|
| `KNOWLEDGE_ID`                     | `machines`                         | logical partition all ingest/query calls land in by default           |
| `FULL_CONTEXT_THRESHOLD`           | `150000`                           | corpora ≤ this many tokens skip retrieval and load whole into prompt  |
| `EMBEDDING_MODEL`                  | `text-embedding-3-small`           | OpenAI                                                                 |
| `GENERATION_MODEL`                 | `claude-sonnet-4-5`                | Anthropic                                                              |
| `VISION_MODEL`                     | `claude-sonnet-4-5`                | Anthropic — drives the drawing pipeline                                |
| `RFNRY_RAG_OBSERVABILITY_FORMAT`   | *(auto)*                           | `pretty` or `json` — overrides the TTY-detection default               |
| `NO_COLOR`                         | *(unset)*                          | disables ANSI color in `PrettyStderrSink`                              |
