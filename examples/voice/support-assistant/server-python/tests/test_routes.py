from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.fixture(autouse=True)
def _env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("PUBLIC_HOST", "tunnel.example.com")


async def _client() -> AsyncClient:
    from src.main import app

    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


async def test_health_returns_ok() -> None:
    async with await _client() as ac:
        r = await ac.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


async def test_twilio_voice_returns_twiml_with_stream_url() -> None:
    async with await _client() as ac:
        r = await ac.post("/twilio/voice")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/xml")
    body = r.text
    assert "<Response>" in body
    assert "<Connect>" in body
    assert "wss://tunnel.example.com/twilio/stream" in body


async def test_kill_unknown_session_returns_ok_no_op() -> None:
    async with await _client() as ac:
        r = await ac.post("/sessions/unknown/kill")
    assert r.status_code == 200


async def test_kill_known_session_calls_manager(monkeypatch: pytest.MonkeyPatch) -> None:
    from src.main import app

    fake = MagicMock()
    fake.kill = AsyncMock()

    original = app.state.manager
    app.state.manager = fake
    try:
        async with await _client() as ac:
            r = await ac.post("/sessions/abc/kill")
    finally:
        app.state.manager = original

    assert r.status_code == 200
    fake.kill.assert_awaited_once_with("abc")


async def test_clear_session_aliased_to_kill(monkeypatch: pytest.MonkeyPatch) -> None:
    from src.main import app

    fake = MagicMock()
    fake.kill = AsyncMock()
    original = app.state.manager
    app.state.manager = fake
    try:
        async with await _client() as ac:
            r = await ac.post("/sessions/abc/clear")
    finally:
        app.state.manager = original

    assert r.status_code == 200
    fake.kill.assert_awaited_once_with("abc")
