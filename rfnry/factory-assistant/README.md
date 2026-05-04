# factory-assistant — rfnry + rfnry-knowledge

A factory technician assistant that combines both libraries: a single
`rfnry` agent whose only tool is a `KnowledgeQuery` call into a local
`rfnry-knowledge` engine indexing **manuals**, **mechanical drawings**,
and **meeting transcripts**. The technician chats over a `thread_id`;
shift leads ingest documents through a separate endpoint. No
front-end — drive it from Postman or curl.

This example demonstrates the two libraries living in one process:
the agent's tool catalog includes a python executor that calls
`KnowledgeEngine.query(...)` directly, with no HTTP hop between them.

## Layout

```
factory-assistant/
├── docker-compose.yml          qdrant + postgres + neo4j + agent
├── documents/                  mock factory documents + PDF renderer
│   ├── md_to_pdf.py            uv-runnable PEP 723 script
│   ├── manual-cnc-mill-mx500.md            (manual)
│   ├── drawing-mx500-spindle-cooling.md    (drawing)
│   └── transcript-incident-2026-04-22.md   (meeting transcript)
└── server-client-python/
    ├── pyproject.toml
    ├── agent/                  rfnry agent root (markdown filetree)
    │   ├── AGENT.md
    │   ├── INDEX.md
    │   ├── rules/
    │   ├── skills/
    │   ├── tools/KnowledgeQuery.md
    │   ├── knowledge/
    │   └── tasks/assist-technician.md
    └── src/
        ├── main.py             FastAPI lifespan wires both engines
        ├── routes.py           /threads/{id}/messages, /ingest, /knowledge, ...
        ├── settings.py         single Settings dataclass
        ├── providers.py        OpenAI embeddings + Anthropic clients (knowledge)
        ├── knowledge_engine.py KnowledgeEngine config + builder
        └── agent/
            ├── server.py       AgentEngine builder
            ├── provider.py     AnthropicProvider for rfnry
            ├── executors.py    knowledge_query python executor
            ├── turn.py
            └── resume.py
```

## How it works

One process hosts both engines. At lifespan startup `main.py` builds
a `KnowledgeEngine` (qdrant + postgres + neo4j) and then an
`AgentEngine` whose `executors={"knowledge_query": ...}` registers a
python callable bound to the live `KnowledgeEngine`. The agent
markdown tree at `server-client-python/agent/` declares one tool
(`tools/KnowledgeQuery.md` with `executor: python`,
`config: {function: knowledge_query}`) so the model can invoke it by
name.

Per ingest:

| `source_type`  | Pipeline                                                                                      |
|----------------|-----------------------------------------------------------------------------------------------|
| `manual`       | text parser -> chunk -> vector + BM25 + Postgres FTS, parent-child on                         |
| `drawing`      | vision LLM (Anthropic) -> component/connection extraction -> vector + graph edges (Neo4j)     |
| `transcript`   | text parser -> chunk -> vector + BM25 + FTS, with `transcript` tag added to source metadata   |

`transcript` routes through the same text path as `manual` — the
distinction is recorded in the source metadata so the agent can cite
the document type correctly.

At query time, multi-path retrieval (vector + document + graph) fuses
with RRF. `QueryMode.AUTO` routes per-query: corpora under
`FULL_CONTEXT_THRESHOLD` skip retrieval and ride the prompt-cached
prefix; larger corpora go through the indexed pipeline. Grounding
gate is on with `threshold=0.4`.

The `thread_id` URL parameter maps directly to the rfnry session id;
each thread's event log lives at
`server-client-python/agent/data/<scope_leaf>/sessions/<thread_id>/events.jsonl`
and is resumable via `POST /threads/{thread_id}/resume`.

## Run

```bash
cd yard/examples/rfnry/factory-assistant

# infra + agent
docker compose up -d
docker compose logs -f agent
```

Or natively:

```bash
docker compose up -d qdrant postgres neo4j

cd server-client-python
cp .env.example .env                       # fill ANTHROPIC_API_KEY + OPENAI_API_KEY
uv sync --extra dev
uv run poe dev                             # http://0.0.0.0:8301
```

## Endpoints

```
POST   /threads/{thread_id}/messages   { "message": "..." }   -> { "thread_id", "reply" }
POST   /threads/{thread_id}/resume                            -> { "thread_id", "reply" }
POST   /ingest                         multipart: file, source_type=manual|drawing|transcript, [knowledge_id], [tags]
GET    /knowledge[?knowledge_id=...]
DELETE /sources/{source_id}
GET    /health
```

## Fixtures

`documents/md_to_pdf.py` is a self-contained uv script (PEP 723); it
has no ties to the server's environment.

```bash
uv run yard/examples/rfnry/factory-assistant/documents/md_to_pdf.py
```

That renders every `*.md` in `documents/` to a sibling `*.pdf`. Drop
more markdown files in there and re-run. The PDFs are committed
alongside their markdown sources — no auto-ingestion, you upload them
through `/ingest`.

## Driving an ingestion + chat

```bash
# ingest manual
curl -X POST http://localhost:8301/ingest \
  -F 'file=@documents/manual-cnc-mill-mx500.pdf' \
  -F 'source_type=manual' \
  -F 'tags=mx-500,milling'

# ingest mechanical drawing
curl -X POST http://localhost:8301/ingest \
  -F 'file=@documents/drawing-mx500-spindle-cooling.pdf' \
  -F 'source_type=drawing' \
  -F 'tags=mx-500,coolant'

# ingest meeting transcript
curl -X POST http://localhost:8301/ingest \
  -F 'file=@documents/transcript-incident-2026-04-22.pdf' \
  -F 'source_type=transcript' \
  -F 'tags=mx-500,incident'

# inspect the corpus
curl http://localhost:8301/knowledge | jq

# start a thread — alarm triage
curl -X POST http://localhost:8301/threads/tech-alice-2026-05-03/messages \
  -H 'content-type: application/json' \
  -d '{"message":"F-411 just popped on MX500-1331 line 3, the spindle housing temp on the HMI looks normal though, what do I do?"}'

# follow up in the same thread — drills into the transcript root cause
curl -X POST http://localhost:8301/threads/tech-alice-2026-05-03/messages \
  -H 'content-type: application/json' \
  -d '{"message":"is this the same thing they reviewed in the april 22 incident?"}'

# different thread — maintenance step lookup
curl -X POST http://localhost:8301/threads/tech-bob-2026-05-03/messages \
  -H 'content-type: application/json' \
  -d '{"message":"what is the target idle drawbar pressure on the MX-500 spindle?"}'

# different thread — procedure walkthrough
curl -X POST http://localhost:8301/threads/tech-carol-2026-05-03/messages \
  -H 'content-type: application/json' \
  -d '{"message":"walk me through the lockout sequence before opening the spindle housing"}'

# resume a thread (replays from the event log if the agent restarted)
curl -X POST http://localhost:8301/threads/tech-alice-2026-05-03/resume

# remove a source
curl -X DELETE http://localhost:8301/sources/<source_id>
```

## Tunables

`server-client-python/.env`:

| key                       | default                              | notes                                                                  |
|---------------------------|--------------------------------------|------------------------------------------------------------------------|
| `ANTHROPIC_MODEL`         | `claude-sonnet-4-6`                  | model the rfnry agent uses for chat                                    |
| `EMBEDDING_MODEL`         | `text-embedding-3-small`             | OpenAI                                                                 |
| `GENERATION_MODEL`        | `claude-sonnet-4-5`                  | Anthropic — knowledge engine answer pass + grounding gate              |
| `VISION_MODEL`            | `claude-sonnet-4-5`                  | Anthropic — drives drawing ingestion                                   |
| `KNOWLEDGE_ID`            | `factory`                            | logical partition all ingest/query calls land in by default            |
| `FULL_CONTEXT_THRESHOLD`  | `150000`                             | corpora <= this many tokens skip retrieval and load whole into prompt  |
