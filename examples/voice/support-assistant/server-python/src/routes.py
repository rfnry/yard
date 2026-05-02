from __future__ import annotations

import json
import os
from collections.abc import AsyncIterator

from fastapi import FastAPI, Request, Response
from rfnry_voice_server.transport import build_twiml_stream
from sse_starlette.sse import EventSourceResponse


def register(app: FastAPI) -> None:
    @app.post("/twilio/voice")
    async def twilio_voice() -> Response:
        host = os.environ.get("PUBLIC_HOST", "")
        ws_url = f"wss://{host}/twilio/stream"
        twiml = build_twiml_stream(ws_url)
        return Response(content=twiml, media_type="text/xml")

    @app.get("/sessions/sse")
    async def sessions_sse(request: Request) -> EventSourceResponse:
        manager = request.app.state.manager

        async def event_stream() -> AsyncIterator[dict[str, str]]:
            async for ids in manager.subscribe_list_changes():
                if await request.is_disconnected():
                    return
                started = {
                    sid: int(manager.started_at(sid).timestamp() * 1000)
                    for sid in ids
                    if manager.started_at(sid) is not None
                }
                yield {"data": json.dumps({"ids": ids, "started_at": started})}

        return EventSourceResponse(event_stream())

    @app.get("/sessions/{session_id}/events/sse")
    async def session_events_sse(
        session_id: str, request: Request
    ) -> EventSourceResponse:
        manager = request.app.state.manager

        async def event_stream() -> AsyncIterator[dict[str, str]]:
            async for ev in manager.subscribe_session_events(session_id):
                if await request.is_disconnected():
                    return
                yield {"data": ev.model_dump_json()}

        return EventSourceResponse(event_stream())

    @app.post("/sessions/{session_id}/kill")
    async def kill_session(session_id: str, request: Request) -> dict[str, bool]:
        await request.app.state.manager.kill(session_id)
        return {"ok": True}

    @app.post("/sessions/{session_id}/clear")
    async def clear_session(session_id: str, request: Request) -> dict[str, bool]:
        # Clearing the agent context — kill + caller will reconnect for a fresh session.
        await request.app.state.manager.kill(session_id)
        return {"ok": True}
