from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any

from composable_agents import AgentConfig, app, deploy
from composable_agents.agent_loop import AgentState, drive_agent_loop
from composable_agents.ir import Node
from composable_agents.registry import DEFAULT_REGISTRY, PureEntry
from conftest import read_snapshot


ROUND_NOTE_NAME = "std.rounds_remaining_note"


def _replace_pure(name: str, fn: Callable[..., Any]) -> PureEntry | None:
    previous = DEFAULT_REGISTRY.pures.pop(name, None)
    DEFAULT_REGISTRY.register_pure(name, fn)
    return previous


def _restore_pure(name: str, previous: PureEntry | None) -> None:
    DEFAULT_REGISTRY.pures.pop(name, None)
    if previous is not None:
        DEFAULT_REGISTRY.pures[name] = previous


def test_round_note_std_pure_adds_remaining_rounds_note_each_round() -> None:
    payloads: list[dict[str, Any]] = []

    async def invoke_controller(payload: dict[str, Any]) -> Any:
        payloads.append(payload)
        if len(payloads) == 1:
            return {"tool": "lookup", "input": {"q": "julep"}}
        return {"output": "done"}

    async def call_tool(actual_tool: str, value: Any) -> Any:
        assert actual_tool == "lookup"
        assert value == {"q": "julep"}
        return {"ok": True}

    out = asyncio.run(
        drive_agent_loop(
            input={"task": "go"},
            cfg=AgentConfig(max_rounds=5, round_note=ROUND_NOTE_NAME),
            invoke_controller=invoke_controller,
            call_tool=call_tool,
        )
    )

    assert out["status"] == "done"
    assert payloads[0]["note"] == "[REMAINING ROUNDS: 5]"
    assert payloads[1]["note"] == "[REMAINING ROUNDS: 4]"


def test_round_note_none_return_omits_note_key() -> None:
    name = "tests.round_note.none"

    def no_note(_ctx: dict[str, Any]) -> None:
        return None

    previous = _replace_pure(name, no_note)
    try:
        payloads: list[dict[str, Any]] = []

        async def invoke_controller(payload: dict[str, Any]) -> Any:
            payloads.append(payload)
            if len(payloads) == 1:
                return {"tool": "lookup", "input": "first"}
            return {"output": "done"}

        async def call_tool(actual_tool: str, value: Any) -> Any:
            assert (actual_tool, value) == ("lookup", "first")
            return {"ok": True}

        out = asyncio.run(
            drive_agent_loop(
                input="q",
                cfg=AgentConfig(max_rounds=3, round_note=name),
                invoke_controller=invoke_controller,
                call_tool=call_tool,
            )
        )
    finally:
        _restore_pure(name, previous)

    assert out["status"] == "done"
    assert payloads
    assert all("note" not in payload for payload in payloads)


def test_round_note_ctx_contains_only_round_budget_spend_and_call_counts() -> None:
    name = "tests.round_note.capture_ctx"
    seen: list[dict[str, Any]] = []

    def capture_ctx(ctx: dict[str, Any]) -> str:
        seen.append(dict(ctx))
        return "captured"

    previous = _replace_pure(name, capture_ctx)
    try:
        payloads: list[dict[str, Any]] = []

        async def invoke_controller(payload: dict[str, Any]) -> Any:
            payloads.append(payload)
            return {"output": "done"}

        async def call_tool(actual_tool: str, value: Any) -> Any:
            raise AssertionError(f"tool should not run: {actual_tool} {value!r}")

        out = asyncio.run(
            drive_agent_loop(
                input={"ignored": True},
                cfg=AgentConfig(max_rounds=5, round_note=name),
                invoke_controller=invoke_controller,
                call_tool=call_tool,
                state=AgentState(
                    round=2,
                    spent=3.5,
                    last={"task": "go"},
                    call_counts={"lookup": 2},
                ),
            )
        )
    finally:
        _restore_pure(name, previous)

    assert out["status"] == "done"
    assert payloads[0]["note"] == "captured"
    assert seen == [
        {
            "round": 2,
            "maxRounds": 5,
            "spent": 3.5,
            "callCounts": {"lookup": 2},
        }
    ]
    assert set(seen[0]) == {"round", "maxRounds", "spent", "callCounts"}


def test_std_rounds_remaining_note_exact_output() -> None:
    note = DEFAULT_REGISTRY.get_pure(ROUND_NOTE_NAME)

    assert note(
        {
            "round": 4,
            "maxRounds": 9,
            "spent": 7.5,
            "callCounts": {"lookup": 2},
        }
    ) == "[REMAINING ROUNDS: 5]"


def test_agent_config_round_note_json_round_trips_and_omits_when_unset() -> None:
    plain_json = AgentConfig().to_json()
    assert "roundNote" not in plain_json

    configured = AgentConfig(round_note=ROUND_NOTE_NAME)
    configured_json = configured.to_json()
    assert configured_json["roundNote"] == ROUND_NOTE_NAME
    assert AgentConfig.from_json(configured_json).round_note == ROUND_NOTE_NAME
    assert AgentConfig.from_json({"round_note": ROUND_NOTE_NAME}).round_note == ROUND_NOTE_NAME
    assert AgentConfig.from_json({}).round_note is None


def test_app_round_note_json_round_trips_and_omits_when_unset() -> None:
    plain = app("ctl")
    assert "roundNote" not in plain.to_json()

    flow = app("ctl", round_note=ROUND_NOTE_NAME)
    encoded = flow.to_json()
    back = Node.from_json(encoded)
    snake_back = Node.from_json(
        {
            "op": "app",
            "id": "app#snake",
            "controller": "ctl",
            "round_note": ROUND_NOTE_NAME,
        }
    )

    assert encoded["roundNote"] == ROUND_NOTE_NAME
    assert back.round_note == ROUND_NOTE_NAME
    assert back.to_json() == encoded
    assert snake_back.round_note == ROUND_NOTE_NAME
    assert snake_back.to_json()["roundNote"] == ROUND_NOTE_NAME


def test_deploy_app_round_note_validates_registration_and_pins_hash() -> None:
    missing = deploy(app("ctl", round_note="not.registered"), read_snapshot(), strict=False)
    missing_unknown = [
        diag
        for diag in missing.diagnostics
        if diag.code == "UNKNOWN_PURE" and "not.registered" in diag.message
    ]

    assert missing_unknown
    assert missing.artifact_components["pureSourceHashes"] == {"not.registered": None}

    valid = deploy(app("ctl", round_note=ROUND_NOTE_NAME), read_snapshot(), strict=False)

    assert not any(diag.code == "UNKNOWN_PURE" for diag in valid.diagnostics)
    assert valid.artifact_components["pureSourceHashes"][ROUND_NOTE_NAME].startswith("pure:")
