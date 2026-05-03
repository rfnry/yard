from __future__ import annotations

import asyncio
import contextlib
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import Any

from rfnry_voice_protocol import DisconnectReason, VoiceEvent


class SessionManager:
    def __init__(self) -> None:
        self._sessions: dict[str, Any] = {}
        self._started_at: dict[str, datetime] = {}
        self._list_subscribers: list[asyncio.Queue[list[str]]] = []

    def register(self, session: Any) -> None:
        self._sessions[session.session_id] = session
        self._started_at[session.session_id] = datetime.now(UTC)
        self._broadcast()

    def unregister(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
        self._started_at.pop(session_id, None)
        self._broadcast()

    def active_ids(self) -> list[str]:
        return list(self._sessions.keys())

    def started_at(self, session_id: str) -> datetime | None:
        return self._started_at.get(session_id)

    async def kill(self, session_id: str) -> None:
        session = self._sessions.get(session_id)
        if session is None:
            return
        with contextlib.suppress(Exception):
            await session._transport.disconnect(reason=DisconnectReason.AGENT_ENDED)

    async def subscribe_list_changes(self) -> AsyncIterator[list[str]]:
        q: asyncio.Queue[list[str]] = asyncio.Queue()
        q.put_nowait(self.active_ids())
        self._list_subscribers.append(q)
        try:
            while True:
                ids = await q.get()
                yield ids
        finally:
            if q in self._list_subscribers:
                self._list_subscribers.remove(q)

    async def subscribe_session_events(
        self, session_id: str
    ) -> AsyncIterator[VoiceEvent]:
        session = self._sessions.get(session_id)
        if session is None:
            return
        async for ev in session.events():
            yield ev

    def _broadcast(self) -> None:
        ids = self.active_ids()
        for q in list(self._list_subscribers):
            q.put_nowait(ids)
