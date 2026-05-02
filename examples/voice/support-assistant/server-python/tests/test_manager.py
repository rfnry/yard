from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import MagicMock

from src.manager import SessionManager


def _make_session(session_id: str) -> Any:
    s = MagicMock()
    s.session_id = session_id

    async def disconnect() -> None:
        return None

    s._transport = MagicMock()
    s._transport.disconnect = disconnect
    return s


async def test_register_and_unregister_track_active_ids() -> None:
    mgr = SessionManager()
    s1 = _make_session("s1")
    mgr.register(s1)
    assert "s1" in mgr.active_ids()
    mgr.unregister("s1")
    assert "s1" not in mgr.active_ids()


async def test_subscribe_list_emits_initial_then_changes() -> None:
    mgr = SessionManager()

    received: list[list[str]] = []

    async def consume() -> None:
        async for ids in mgr.subscribe_list_changes():
            received.append(list(ids))
            if len(received) >= 2:
                return

    consumer = asyncio.create_task(consume())
    await asyncio.sleep(0.01)

    mgr.register(_make_session("s1"))
    await asyncio.wait_for(consumer, timeout=1.0)

    assert received[0] == []
    assert "s1" in received[1]


async def test_kill_unknown_session_is_noop() -> None:
    mgr = SessionManager()
    await mgr.kill("nope")  # must not raise
