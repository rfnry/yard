from __future__ import annotations

import contextlib
import uuid

from fastapi import FastAPI, WebSocket
from rfnry_voice_server.transport import TwilioMediaStreamTransport

from src.agent import make_session
from src.tools import register_tool_handlers


class _TwilioWSAdapter:
    """Adapt FastAPI's WebSocket to the receive_text/send_text/close shape Twilio uses."""

    def __init__(self, ws: WebSocket) -> None:
        self._ws = ws

    async def receive_text(self) -> str:
        return await self._ws.receive_text()

    async def send_text(self, data: str) -> None:
        await self._ws.send_text(data)

    async def close(self) -> None:
        with contextlib.suppress(Exception):
            await self._ws.close()


def register(app: FastAPI) -> None:
    @app.websocket("/twilio/stream")
    async def twilio_stream(ws: WebSocket) -> None:
        await ws.accept()
        adapter = _TwilioWSAdapter(ws)
        transport = TwilioMediaStreamTransport(websocket=adapter)
        session_id = uuid.uuid4().hex[:12]
        session = make_session(session_id=session_id, transport=transport)
        register_tool_handlers(session)
        ws.app.state.manager.register(session)
        try:
            await session.run()
        finally:
            ws.app.state.manager.unregister(session.session_id)
