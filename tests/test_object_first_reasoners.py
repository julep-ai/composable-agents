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


def test_deploy_registers_reasoner_object_and_wire_is_identical() -> None:
    from composable_agents import Reasoner, deploy, flow, pure, think, tool

    @tool(effect="read", idempotent=True)
    def lookup(t: str) -> dict:
        return {"q": "billing"}

    @pure("ws5_prompt2")
    def prompt(hit: dict) -> dict:
        return {"q": hit["q"]}

    r = Reasoner(name="ws5_reply2", model="anthropic:claude-haiku-4-5-20251001",
                 system="x", reply={"reply": "str"})

    @flow
    def triage(t: str) -> dict:
        hit = lookup(t)
        return prompt(hit) | think(r, prompt(hit))

    # Object-first: no register_reasoner call anywhere.
    dep = deploy(triage, tools=[lookup], reasoners=[r])
    dep_by_name = deploy(triage, tools=[lookup], reasoners=[r.name])
    assert dep.artifact_hash  # froze successfully
    assert "ws5_reply2" in dep.artifact_components["reasoners"]  # name landed in the artifact
    assert dep.artifact_components == dep_by_name.artifact_components
