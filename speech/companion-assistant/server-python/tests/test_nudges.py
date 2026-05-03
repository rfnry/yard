from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from typing import Any
from unittest.mock import AsyncMock

from rfnry_voice_protocol import TranscriptUserFinalEvent, VoiceEvent

from src.nudges import SilenceNudger


class _FakeSession:
    def __init__(self) -> None:
        self._queue: asyncio.Queue[VoiceEvent] = asyncio.Queue()
        self._closed = False

    async def push(self, ev: VoiceEvent) -> None:
        await self._queue.put(ev)

    def close(self) -> None:
        self._closed = True

    async def events(self) -> AsyncIterator[VoiceEvent]:
        while True:
            if self._closed and self._queue.empty():
                return
            try:
                ev = await asyncio.wait_for(self._queue.get(), timeout=0.05)
            except TimeoutError:
                if self._closed:
                    return
                continue
            yield ev


def _user_final(text: str = "hi") -> VoiceEvent:
    return TranscriptUserFinalEvent(
        id="e",
        timestamp_ms=0,
        session_id="s",
        scope={},
        speaker_id="caller",
        text=text,
    )


async def test_nudge_fires_after_silence_threshold() -> None:
    session = _FakeSession()
    sts: Any = AsyncMock()
    nudger = SilenceNudger(session, sts, silence_s=0.1)
    task = asyncio.create_task(nudger.run())
    await asyncio.sleep(0.25)
    session.close()
    await task
    sts.send_text.assert_called()


async def test_nudge_resets_on_user_transcript() -> None:
    session = _FakeSession()
    sts: Any = AsyncMock()
    nudger = SilenceNudger(session, sts, silence_s=0.15)
    task = asyncio.create_task(nudger.run())
    # Push a user transcript before the timer expires
    await asyncio.sleep(0.05)
    await session.push(_user_final())
    # No nudge should fire in this short window
    await asyncio.sleep(0.05)
    sts.send_text.assert_not_called()
    session.close()
    await task


async def test_no_nudge_after_session_ends() -> None:
    session = _FakeSession()
    sts: Any = AsyncMock()
    nudger = SilenceNudger(session, sts, silence_s=0.5)
    task = asyncio.create_task(nudger.run())
    session.close()
    await task
    sts.send_text.assert_not_called()
