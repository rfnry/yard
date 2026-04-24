"""FastAPI server exposing every agent under ./agents/ at the same shape.

Routes:
  POST /agents/<path>/chat        {session_id, message, scope?, task?}
  POST /agents/<path>/resume      {session_id, scope?, task?}
  POST /agents/<path>/consolidate {task, scope?}
  GET  /agents/<path>/events      session events tail
  GET  /agents                    list of available agents

Path is `<agent>/<tier>`, e.g. `stock-agent/minimal`. The server resolves it
relative to ./agents/. Namespaces are inferred: paths containing
`self-evolving` use ["org_id"]; others use [].

Provider is chosen via PROVIDER env var: mock (default), anthropic, openai.
Real providers require ANTHROPIC_API_KEY / OPENAI_API_KEY.

Run:
  cd examples/python
  uv sync && uv run uvicorn server:app --reload
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from rfnry.agent.core import Agent
from rfnry.host.events import EventLog
from rfnry.refining.config import RefiningConfig

AGENTS_ROOT = Path(__file__).parent / "agents"
PROVIDER_KIND = os.environ.get("PROVIDER", "mock")

app = FastAPI(title="rfnry agents demo")


def _build_provider() -> Any:
    if PROVIDER_KIND == "mock":
        from rfnry.providers.mock import MockProvider

        return MockProvider()
    if PROVIDER_KIND == "anthropic":
        from anthropic import AsyncAnthropic

        from rfnry.providers.anthropic import AnthropicProvider

        return AnthropicProvider(
            client=AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"]),
            model=os.environ.get("MODEL", "claude-sonnet-4-6"),
        )
    if PROVIDER_KIND == "openai":
        from openai import AsyncOpenAI

        from rfnry.providers.openai import OpenAIProvider

        return OpenAIProvider(
            client=AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"]),
            model=os.environ.get("MODEL", "gpt-4o-mini"),
        )
    raise ValueError(f"unknown PROVIDER: {PROVIDER_KIND}")


_AGENTS: dict[str, Agent] = {}


def _get_agent(path: str) -> Agent:
    if path in _AGENTS:
        return _AGENTS[path]
    agent_root = (AGENTS_ROOT / path).resolve()
    if AGENTS_ROOT.resolve() not in agent_root.parents:
        raise HTTPException(status_code=400, detail="path escapes agents/")
    if not agent_root.is_dir() or not (agent_root / "AGENT.md").exists():
        raise HTTPException(status_code=404, detail=f"no agent at {path}")
    namespaces = ["org_id"] if "self-evolving" in path else []
    provider = _build_provider()
    agent = Agent(
        root=agent_root,
        provider=provider,
        namespaces=namespaces,
        refining=RefiningConfig(provider=provider),
    )
    _AGENTS[path] = agent
    return agent


class ChatBody(BaseModel):
    session_id: str
    message: str = ""
    scope: dict[str, str] = {}
    task: str | None = None


class ConsolidateBody(BaseModel):
    task: str
    scope: dict[str, str] = {}


@app.get("/agents")
def list_agents() -> dict[str, list[str]]:
    paths: list[str] = []
    if not AGENTS_ROOT.exists():
        return {"agents": paths}
    for agent in sorted(AGENTS_ROOT.iterdir()):
        if not agent.is_dir() or agent.name.startswith((".", "_")):
            continue
        for tier in sorted(agent.iterdir()):
            if tier.is_dir() and (tier / "AGENT.md").exists():
                paths.append(f"{agent.name}/{tier.name}")
    return {"agents": paths}


@app.post("/agents/{agent_path:path}/chat")
async def chat(agent_path: str, body: ChatBody) -> dict[str, str]:
    agent = _get_agent(agent_path)
    reply = await agent.turn(
        session_id=body.session_id,
        message=body.message,
        scope=body.scope,
        task=body.task,
    )
    return {"reply": reply}


@app.post("/agents/{agent_path:path}/resume")
async def resume(agent_path: str, body: ChatBody) -> dict[str, str]:
    agent = _get_agent(agent_path)
    reply = await agent.resume(
        session_id=body.session_id,
        scope=body.scope,
        task=body.task,
    )
    return {"reply": reply}


@app.post("/agents/{agent_path:path}/consolidate")
async def consolidate(agent_path: str, body: ConsolidateBody) -> dict[str, Any]:
    agent = _get_agent(agent_path)
    result = await agent.consolidate(task=body.task, scope=body.scope)
    return {
        "promoted": [p.name for p in result.promoted],
        "rejected": result.rejected,
        "event": result.event.model_dump(mode="json"),
    }


@app.get("/agents/{agent_path:path}/events")
async def events(agent_path: str, session_id: str, scope_leaf: str = "_default") -> dict[str, Any]:
    agent_root = (AGENTS_ROOT / agent_path).resolve()
    if not agent_root.is_dir():
        raise HTTPException(status_code=404, detail=f"no agent at {agent_path}")
    log_path = agent_root / "data" / scope_leaf / "sessions" / session_id / "events.jsonl"
    if not log_path.exists():
        return {"events": []}
    log = EventLog(path=log_path)
    tail = await log.tail(n=50)
    return {"events": [e.model_dump(mode="json") for e in tail]}
