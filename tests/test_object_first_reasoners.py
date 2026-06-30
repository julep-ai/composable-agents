from typing import TypedDict

import pytest

from composable_agents import Reasoner


class Reply(TypedDict):
    answer: str


def test_reply_accepts_typeddict() -> None:
    r = Reasoner(name="r1", model="anthropic:claude-haiku-4-5-20251001", reply=Reply)
    assert isinstance(r.reply_schema, dict) and r.reply_schema  # materialized schema


def test_reply_accepts_raw_schema_dict() -> None:
    schema = {"regime": "str", "confidence": "number"}
    r = Reasoner(name="r2", model="anthropic:claude-haiku-4-5-20251001", reply=schema)
    assert r.reply_schema == schema  # raw dict stored as-is


def test_reply_schema_kwarg_is_gone() -> None:
    with pytest.raises(TypeError):
        Reasoner(  # type: ignore[call-arg]
            name="r3", model="anthropic:claude-haiku-4-5-20251001",
            reply_schema={"answer": "str"},
        )
