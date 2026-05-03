from __future__ import annotations

from src.agent import build_instructions
from src.memory import CompanionContext, CompanionTurn


def test_build_instructions_includes_companion_and_user_name() -> None:
    ctx = CompanionContext(name="alice", summary="", recent_turns=[])
    text = build_instructions(companion_name="Sam", ctx=ctx)
    assert "Sam" in text
    assert "alice" in text


def test_build_instructions_includes_summary_when_present() -> None:
    ctx = CompanionContext(
        name="alice",
        summary="alice mentioned she likes hiking",
        recent_turns=[],
    )
    text = build_instructions(companion_name="Sam", ctx=ctx)
    assert "alice mentioned she likes hiking" in text


def test_build_instructions_includes_recent_turns() -> None:
    ctx = CompanionContext(
        name="alice",
        summary="",
        recent_turns=[
            CompanionTurn(speaker_id="user", text="how was your day?"),
            CompanionTurn(speaker_id="agent", text="weird, but you?"),
        ],
    )
    text = build_instructions(companion_name="Sam", ctx=ctx)
    assert "how was your day?" in text
    assert "weird, but you?" in text


def test_build_instructions_no_history_uses_empty_section() -> None:
    ctx = CompanionContext(name="alice", summary="", recent_turns=[])
    text = build_instructions(companion_name="Sam", ctx=ctx)
    assert "no prior conversation" in text.lower()
