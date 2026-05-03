# recipe-collector — rfnry-rag + forge-parser example

A small recipe-management RAG that demonstrates **forge-parser** as a
fidelity guardrail on top of `rfnry-rag` ingestion.

Recipes are the canonical hard domain in the DELEGATE-52 paper for
silent corruption — "200 g of butter" silently becomes "800 g of
butter" and nobody notices until someone bakes. RAG ingestion adds
its own corruption surface: chunking can split an ingredient list,
LLM-driven enrichment (document expansion, contextual chunks) can
introduce subtle drift, and retrieval can return chunks that don't
contain the full ingredient.

This example registers a custom `recipe` parser into
`rfnry_forge.parser.default_registry`, ingests three recipe markdowns
through `rfnry-rag`, and exposes a `/verify-source` endpoint that
parses both the original file and the chunks-as-stored, then surfaces
deletion/corruption deltas.

## Why this example

- The smallest end-to-end test of `rfnry-rag` + `rfnry-forge-parser`.
- Demonstrates the **consumer-extension** path: registering a
  domain-specific parser into the default registry.
- Demonstrates the **ingestion fidelity** check: comparing the raw
  source to the chunked-and-stored representation via parser counts.
- Provides realistic input: three recipe markdowns rendered to PDF
  via the same `md_to_pdf.py` script the operation-assistant uses.

## Layout

```
recipe-collector/
├── documents/
│   ├── md_to_pdf.py                renders *.md to *.pdf
│   ├── recipe-eclair.md
│   ├── recipe-pasta-carbonara.md
│   └── recipe-thai-curry.md
├── python/
│   └── src/
│       ├── main.py                 FastAPI server
│       ├── routes.py               /ingest /query /verify-source
│       ├── rag.py                  RagEngine config
│       ├── recipe_parser.py        the custom forge-parser
│       └── schemas.py              request/response models
└── docker-compose.yml              postgres + qdrant
```

## Run

```bash
# 1. infra
docker compose up -d

# 2. render the seed recipes to PDF
cd documents
uv run md_to_pdf.py
cd ..

# 3. server
cd python
cp .env.example .env       # set ANTHROPIC_API_KEY, OPENAI_API_KEY
uv sync --extra dev
uv run poe dev             # 8105
```

## Endpoints

```
POST /ingest         multipart with file=<recipe.pdf>, source_type=recipe
POST /query          { "query": "what's in the carbonara?" }
POST /verify-source  { "source_id": "...", "raw_path": "documents/recipe-...md" }
GET  /knowledge      list ingested sources
GET  /health
```

## What `/verify-source` does

1. Loads the raw markdown from `raw_path`.
2. Loads every chunk that rfnry-rag stored for `source_id` from the
   document store.
3. Concatenates the chunks back into a single text body.
4. Parses both with the registered `recipe` parser.
5. Computes `parser.diff(raw_parsed, stored_parsed)` and returns the
   `StructuralDelta`: deletion paths (missing ingredients), corruption
   paths (changed quantities), count drift.

The output is a small JSON document the consumer can show in a UI:
"recipe-eclair.md: stored has 2 fewer ingredients than the source —
['butter', 'eggs']."

## What this catches

- **Chunker boundary loss.** If the chunker split mid-ingredient and
  one half got dropped during dedup, `deletion_paths` shows it.
- **OCR / parsing drift.** If ingestion went through a vision model
  (PDF → text), numeric corruption (`200g` → `2000g`) shows in
  `corruption_paths`.
- **Source-storage mismatch.** If the document store stored a
  different version than the chunker saw, the count drift is the
  signal.

## What this does NOT catch (yet)

- Generation-time corruption (the LLM hallucinating an ingredient in
  the answer). That needs a separate verify-against-grounded-sources
  step at query time. v0.0.2 candidate.
- Cross-recipe leakage (chunk from recipe A retrieved when querying
  recipe B). That's a retrieval-precision concern; the existing
  rfnry-rag trace already surfaces it.

## Notes

- Recipe parser is intentionally simple: it picks up the
  `## INGREDIENTS` section as a list of `(quantity, unit, name)`
  triples and the `## STEPS` / `## METHOD` section as numbered
  procedures. Real recipe parsing is harder; the goal here is to
  show the registration shape.
- This is the smallest viable rag wiring — vector + document stores
  only, no graph, no drawing pipeline. See `operation-assistant` for
  a fuller setup.
