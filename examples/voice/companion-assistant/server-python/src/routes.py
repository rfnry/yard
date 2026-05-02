from __future__ import annotations

import asyncio
import contextlib
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from rfnry_voice_server.exceptions import NamespaceViolation
from rfnry_voice_server.sandbox.scopes import validate_safe_segment
from rfnry_voice_server.transport import WebRTCTransport, accept_offer

from src.agent import make_session
from src.nudges import SilenceNudger


class OfferBody(BaseModel):
    sdp: str
    type: str


class AnswerBody(BaseModel):
    sdp: str
    type: str


def register(app: FastAPI) -> None:
    @app.post("/webrtc/offer/{user_name}", response_model=AnswerBody)
    async def webrtc_offer(
        user_name: str, body: OfferBody, request: Request
    ) -> AnswerBody:
        try:
            validate_safe_segment(user_name)
        except NamespaceViolation as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        memory = request.app.state.memory
        transport = WebRTCTransport()
        answer = await accept_offer(transport, sdp=body.sdp, type=body.type)
        session = make_session(user_name=user_name, memory=memory, transport=transport)

        sts_session = _peek_sts_session(session)

        # Wire memory persistence on transcript events.
        @session.on("transcript.user.final")
        async def _record_user(ctx: Any, send: Any) -> None:
            memory.append(user_name, speaker="user", text=ctx.event.text)

        @session.on("transcript.agent.final")
        async def _record_agent(ctx: Any, send: Any) -> None:
            memory.append(user_name, speaker="agent", text=ctx.event.text)

        async def _runner() -> None:
            tasks: list[asyncio.Task[Any]] = [asyncio.create_task(session.run())]
            if sts_session is not None:
                nudger = SilenceNudger(session, sts_session)
                tasks.append(asyncio.create_task(nudger.run()))
            with contextlib.suppress(Exception):
                await asyncio.gather(*tasks, return_exceptions=True)

        asyncio.create_task(_runner())
        return AnswerBody(sdp=answer.sdp, type=answer.type)


def _peek_sts_session(_session: Any) -> Any | None:
    # The STS session is opened lazily inside VoiceSession.run(); the nudger needs
    # a handle to send_text. For MVP, leave as None — the nudger code is robust to
    # a missing sts_session (suppresses send errors) and the underlying loop still
    # runs. Wiring a real handle requires touching VoiceSession internals; the host
    # can do that in a richer integration.
    return None
