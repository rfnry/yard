from __future__ import annotations

import asyncio
import contextlib
from typing import Any

NUDGE_PROMPT = (
    "The user has been quiet for a while. Say something natural to re-engage — a "
    "follow-up question, a small observation, or a gentle prompt. Do not announce "
    "that you noticed silence; just speak."
)


class SilenceNudger:
    def __init__(self, session: Any, sts_session: Any, *, silence_s: float = 25.0) -> None:
        self._session = session
        self._sts_session = sts_session
        self._silence_s = silence_s
        self._last_user_activity = 0.0
        self._stop = asyncio.Event()

    async def run(self) -> None:
        self._last_user_activity = asyncio.get_event_loop().time()
        consumer = asyncio.create_task(self._consume_events())
        try:
            while not self._stop.is_set():
                now = asyncio.get_event_loop().time()
                idle = now - self._last_user_activity
                if idle >= self._silence_s:
                    with contextlib.suppress(Exception):
                        await self._sts_session.send_text(NUDGE_PROMPT)
                    self._last_user_activity = now
                await asyncio.sleep(min(self._silence_s / 4, 0.05))
                if consumer.done():
                    break
        finally:
            self._stop.set()
            consumer.cancel()
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await consumer

    async def _consume_events(self) -> None:
        async for ev in self._session.events():
            if ev.type in ("transcript.user.partial", "transcript.user.final"):
                self._last_user_activity = asyncio.get_event_loop().time()
        self._stop.set()
