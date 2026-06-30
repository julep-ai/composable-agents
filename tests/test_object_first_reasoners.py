import subprocess
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


def test_agent_accepts_reasoner_object() -> None:
    from composable_agents import Agent, Reasoner

    r = Reasoner(name="ws5_ctrl", model="anthropic:claude-haiku-4-5-20251001", reply={"out": "str"})
    agent = Agent(reasoner=r)                 # object, not a string, no prior registration
    # the agent resolved the reasoner by name under the hood
    assert agent is not None


def test_register_reasoner_not_public() -> None:
    import composable_agents

    assert not hasattr(composable_agents, "register_reasoner")
    assert "register_reasoner" not in composable_agents.__all__


def test_think_accepts_object_at_authoring_time() -> None:
    from composable_agents import Reasoner, flow, pure, think, tool

    @tool(effect="read", idempotent=True)
    def lk(t: str) -> dict:
        return {"q": "b"}

    @pure("ws5_p4")
    def pp(h: dict) -> dict:
        return {"q": h["q"]}

    r = Reasoner(name="ws5_think_obj", model="anthropic:claude-haiku-4-5-20251001", reply={"o": "str"})

    @flow
    def f(t: str) -> dict:
        return pp(lk(t)) | think(r, pp(lk(t)))

    assert f is not None  # @flow define-time accepted think(r, ...)


def test_no_public_register_reasoner_or_reply_schema_left() -> None:
    # register_reasoner must not appear as a public/import symbol; reply_schema must
    # not appear as a constructor kwarg anywhere in package, examples, docs, or the
    # user-facing README/CONTRIBUTING (the PyPI landing page included).
    out = subprocess.run(
        ["grep", "-rn", "register_reasoner\\|reply_schema=",
         "composable_agents", "examples", "docs-site/content", "README.md", "CONTRIBUTING.md"],
        capture_output=True, text=True,
    ).stdout
    # The only allowed hit is the internal registry method definition.
    leftovers = [
        ln for ln in out.splitlines()
        if "DEFAULT_REGISTRY.register_reasoner" not in ln
        and "def register_reasoner(self" not in ln
    ]
    assert not leftovers, "leftover register_reasoner/reply_schema=: \n" + "\n".join(leftovers)
