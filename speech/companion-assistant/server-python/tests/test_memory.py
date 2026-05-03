from __future__ import annotations

from src.memory import CompanionMemory


def test_get_unknown_user_returns_empty_context() -> None:
    mem = CompanionMemory()
    ctx = mem.get("alice")
    assert ctx.name == "alice"
    assert ctx.summary == ""
    assert ctx.recent_turns == []


def test_append_records_turns_in_order() -> None:
    mem = CompanionMemory()
    mem.append("alice", speaker="user", text="hi")
    mem.append("alice", speaker="agent", text="hello there")
    ctx = mem.get("alice")
    assert len(ctx.recent_turns) == 2
    assert ctx.recent_turns[0].speaker_id == "user"
    assert ctx.recent_turns[1].text == "hello there"


def test_max_turns_drops_oldest() -> None:
    mem = CompanionMemory(max_turns=3)
    for i in range(5):
        mem.append("alice", speaker="user", text=f"m{i}")
    ctx = mem.get("alice")
    assert len(ctx.recent_turns) == 3
    assert ctx.recent_turns[0].text == "m2"
    assert ctx.recent_turns[-1].text == "m4"


def test_reset_clears_user_state() -> None:
    mem = CompanionMemory()
    mem.append("alice", speaker="user", text="hi")
    mem.reset("alice")
    assert mem.get("alice").recent_turns == []


def test_isolation_between_users() -> None:
    mem = CompanionMemory()
    mem.append("alice", speaker="user", text="hi from alice")
    mem.append("bob", speaker="user", text="hi from bob")
    a = mem.get("alice")
    b = mem.get("bob")
    assert len(a.recent_turns) == 1
    assert a.recent_turns[0].text == "hi from alice"
    assert len(b.recent_turns) == 1
    assert b.recent_turns[0].text == "hi from bob"
