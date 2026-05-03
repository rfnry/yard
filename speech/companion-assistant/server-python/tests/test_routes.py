from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.fixture(autouse=True)
def _env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")


async def _client() -> AsyncClient:
    from src.main import app

    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


async def test_health_returns_ok() -> None:
    async with await _client() as ac:
        r = await ac.get("/health")
    assert r.status_code == 200


async def test_webrtc_offer_rejects_unsafe_user_name_segment() -> None:
    async with await _client() as ac:
        r = await ac.post(
            "/webrtc/offer/..%2Fbad",
            json={"sdp": "v=0\n", "type": "offer"},
        )
    # FastAPI may decode the path; accept either 4xx
    assert r.status_code in (400, 404, 422)


async def test_webrtc_offer_validates_payload_shape() -> None:
    async with await _client() as ac:
        r = await ac.post("/webrtc/offer/alice", json={"sdp": "x"})
    assert r.status_code == 422  # missing 'type'
