# multi-tenant — agent for organization-b

Standalone agent that connects to the multi-tenant chat server and serves **organization-b** (both `workspace-b-1` and `workspace-b-2`).

- Identity: `AssistantIdentity(id="agent-b", name="Agent B", metadata={"tenant": {"organization": "organization-b", "workspace": "*", "author": "*"}})`.
- The `"*"` wildcards on `workspace` and `author` mean a single agent process spans both workspaces and sees every user's threads, while staying cleanly scoped to organization-b.
- Agent discovers threads via `ChatClient.run(on_connect=...)` + a 10s poll loop — it never needs to be added as a thread member. See [`../README.md`](../README.md) for the full model.

## Layout

```
src/
  main.py      asyncio entry — connects a ChatClient, runs the discovery poller
  agent.py     identity + @on_message handler
  provider.py  Anthropic SDK glue
```

## Run

```bash
cd yard/examples/rfnry-chat/multi-tenant/client-python-b
cp .env.example .env    # then fill in ANTHROPIC_API_KEY (optional) and CHAT_SERVER_URL
uv sync --extra dev

uv run poe dev          # start the agent (= `python -m src.main`)
```

## Development

Dev tooling via [`poethepoet`](https://poethepoet.natn.io/) (tasks declared in `pyproject.toml`, `[tool.poe.tasks]`).

```bash
uv sync --extra dev           # install ruff + mypy + poethepoet

uv run poe dev                # run the agent (`python -m src.main`)
uv run poe start              # same (kept for symmetry with server examples)
uv run poe format             # ruff format .
uv run poe format:imports     # ruff check --select I --fix .
uv run poe check              # ruff check .
uv run poe check:fix          # ruff check --fix .
uv run poe typecheck          # mypy src
```
