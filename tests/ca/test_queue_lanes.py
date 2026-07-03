from __future__ import annotations

import io
from importlib import import_module
from pathlib import Path
from typing import Any

import pytest

from composable_agents import Agent, Shape, tool
from composable_agents.ca.config import CaConfig, EnvConfig, load_config
from composable_agents.ca.ledger import DeployRecord, upsert_records
from composable_agents.ca.queues import queue_lane_diagnostics, resolve_queue_lane
from composable_agents.ca.temporal_run import build_flow_start_args, run_on_env
from composable_agents.execution.harness import (
    AgentInput,
    FlowInput,
    _resolve_child_queue,
)
from composable_agents.ir import Node, Op, SubContract, SubStep
from composable_agents.typed import as_flow


def _record(*, queue: str | None = None) -> DeployRecord:
    return DeployRecord(
        agent="triage",
        artifact_hash="sha256:deadbeef",
        flow_json={"op": "arr", "id": "n", "pure": "std.identity"},
        manifest_json={"tools": []},
        bundle_ref=None,
        pinned_pures={},
        queue=queue,
        deployed_at="2026-07-03T00:00:00+00:00",
    )


def test_config_parse_queues_and_default_lane_resolution(tmp_path: Path) -> None:
    (tmp_path / "ca.toml").write_text(
        "[env.prod]\n"
        'task_queue = "prod-default"\n'
        "[env.prod.queues]\n"
        'foreground = "prod-fg"\n',
        encoding="utf-8",
    )

    cfg = load_config(tmp_path)

    assert cfg.envs["prod"].queues == {"foreground": "prod-fg"}
    assert resolve_queue_lane(None, cfg.envs["prod"].queues, "prod-default") == "prod-default"
    assert resolve_queue_lane("foreground", cfg.envs["prod"].queues, "prod-default") == "prod-fg"
    assert resolve_queue_lane("raw-q", cfg.envs["prod"].queues, "prod-default") == "raw-q"


def test_deploy_record_queue_omit_and_roundtrip() -> None:
    base = _record()
    expected = {
        "agent": "triage",
        "artifact_hash": "sha256:deadbeef",
        "flow_json": {"op": "arr", "id": "n", "pure": "std.identity"},
        "manifest_json": {"tools": []},
        "bundle_ref": None,
        "pinned_pures": {},
        "deployed_at": "2026-07-03T00:00:00+00:00",
    }

    assert base.to_json() == expected
    assert DeployRecord.from_json(expected).queue is None

    queued = _record(queue="foreground")
    encoded = queued.to_json()
    assert encoded["queue"] == "foreground"
    assert DeployRecord.from_json(encoded).queue == "foreground"


def test_ir_subflow_contract_queue_omit_and_roundtrip() -> None:
    base = SubContract(shape=Shape.PIPELINE)
    assert base.to_json() == {"shape": Shape.PIPELINE.value}
    assert SubContract.from_json(base.to_json()) == base

    queued = SubContract(shape=Shape.PIPELINE, queue="fg")
    encoded = queued.to_json()
    assert encoded["queue"] == "fg"
    assert SubContract.from_json(encoded) == queued


def test_ca_run_resolves_lane_and_carries_lane_map(tmp_path: Path) -> None:
    env = EnvConfig(
        name="prod",
        temporal_address="temporal.prod:7233",
        task_queue="prod-default",
        queues={"foreground": "prod-fg"},
    )
    cfg = CaConfig(root=tmp_path, envs={"prod": env})
    upsert_records(tmp_path, "prod", [_record(queue="foreground")])
    captured: dict[str, Any] = {}

    def spy_run_flow(client: Any, flow_json: Any, manifest_json: Any, **kwargs: Any) -> str:
        captured["kwargs"] = kwargs
        captured["flow_json"] = flow_json
        captured["manifest_json"] = manifest_json
        return "ok"

    assert run_on_env(cfg, "triage", env, {"ticket": "T"}, client=object(), run_flow=spy_run_flow) == "ok"
    assert captured["kwargs"]["task_queue"] == "prod-fg"
    assert captured["kwargs"]["queue_lanes"] == {"foreground": "prod-fg"}

    upsert_records(tmp_path, "prod", [_record(queue=None)])
    run_on_env(cfg, "triage", env, None, client=object(), run_flow=spy_run_flow)
    assert captured["kwargs"]["task_queue"] == "prod-default"

    sa = build_flow_start_args(_record(queue="foreground"), env, None)
    assert sa.task_queue == "prod-fg"
    assert sa.queue_lanes == {"foreground": "prod-fg"}


def test_child_start_resolution_matrix() -> None:
    assert _resolve_child_queue(None, {"fg": "prod-fg"}) is None
    assert _resolve_child_queue("fg", {"fg": "prod-fg"}) == "prod-fg"
    assert _resolve_child_queue("weird", {"fg": "prod-fg"}) == "weird"
    assert _resolve_child_queue("fg", None) == "fg"


def test_queue_lanes_transitive_propagation_and_can_preservation() -> None:
    lanes = {"foreground": "ca-fg"}
    parent = FlowInput(session_id="p", flow_json={}, queue_lanes=lanes)

    child_contract = SubContract(shape=Shape.PIPELINE, queue="foreground")
    child = FlowInput(
        session_id="c",
        input="v",
        ref="child",
        queue_lanes=(parent.queue_lanes or None),
    )
    assert child.queue_lanes == lanes
    assert _resolve_child_queue(child_contract.queue, child.queue_lanes) == "ca-fg"

    grandchild = FlowInput(
        session_id="g",
        input="v",
        ref="grandchild",
        queue_lanes=(child.queue_lanes or None),
    )
    assert grandchild.queue_lanes == lanes
    assert _resolve_child_queue("foreground", grandchild.queue_lanes) == "ca-fg"

    flow_can = FlowInput(
        session_id=parent.session_id,
        input="next",
        flow_json=parent.flow_json,
        queue_lanes=parent.queue_lanes,
    )
    assert flow_can.queue_lanes == lanes

    agent = AgentInput(
        controller="ctrl",
        session_id="a",
        queue_lanes=lanes,
        subflow_queues={"child": "foreground"},
    )
    agent_can = AgentInput(
        controller=agent.controller,
        session_id=agent.session_id,
        queue_lanes=agent.queue_lanes,
        subflow_queues=agent.subflow_queues,
        resolve_spec=False,
    )
    assert agent_can.queue_lanes == lanes
    assert agent_can.subflow_queues == {"child": "foreground"}


def test_worker_queue_cli_resolves_lanes_and_raw_strings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import composable_agents.cli as cli

    serve_mod = import_module("composable_agents.execution.serve")

    (tmp_path / "ca.toml").write_text(
        "[env.prod]\n"
        'task_queue = "prod-default"\n'
        "[env.prod.queues]\n"
        'foreground = "prod-fg"\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    captured: list[str] = []

    async def fake_serve(settings: Any) -> None:
        captured.append(settings.task_queue)

    monkeypatch.setattr(serve_mod, "serve", fake_serve)
    parser = cli._parser()

    args = parser.parse_args(
        ["worker", "--context-factory", "m:f", "--queue", "foreground", "--env", "prod"]
    )
    assert cli._cmd_worker(args, io.StringIO()) == 0
    assert captured[-1] == "prod-fg"

    args = parser.parse_args(
        ["worker", "--context-factory", "m:f", "--queue", "raw-q", "--env", "prod"]
    )
    assert cli._cmd_worker(args, io.StringIO()) == 0
    assert captured[-1] == "raw-q"


def test_queue_lane_diagnostics_for_agent_and_ir_subcontracts() -> None:
    @tool(effect="read", idempotent=True, name="ql_diag_tool")
    def child_tool(value: str) -> str:
        return value

    child = Agent("m", tools=[child_tool], name="ql_diag_child")
    typo_parent = Agent(
        "m",
        tools=[child.as_sub(queue="typo")],
        name="ql_diag_parent_typo",
    )
    configured_parent = Agent(
        "m",
        tools=[child.as_sub(queue="foreground")],
        name="ql_diag_parent_ok",
    )

    diagnostics = queue_lane_diagnostics(
        typo_parent,
        {"foreground": "prod-fg"},
        "prod",
    )
    assert len(diagnostics) == 1
    assert diagnostics[0]["code"] == "QUEUE_UNKNOWN_LANE"
    assert diagnostics[0]["severity"] == "error"
    assert "foreground" in diagnostics[0]["message"]

    assert queue_lane_diagnostics(configured_parent, {"foreground": "prod-fg"}, "prod") == []
    assert queue_lane_diagnostics(typo_parent, {}, "prod") == []

    ir_found = as_flow(
        Node(
            op=Op.PRIM,
            id="sub_1",
            step=SubStep("child", SubContract(Shape.PIPELINE, queue="typo")),
        )
    )
    ir_diags = queue_lane_diagnostics(ir_found, {"foreground": "prod-fg"}, "prod")
    assert [diag["code"] for diag in ir_diags] == ["QUEUE_UNKNOWN_LANE"]


def test_resolve_agent_spec_subflow_queues_passthrough() -> None:
    from conftest import run

    from composable_agents.execution import effects
    from composable_agents.execution.effects import WorkerContext, configure

    prev = effects._CTX
    configure(
        WorkerContext(
            agents={
                "ctrl": {"subflowQueues": {"child": "fg"}},
                "plain": {},
            }
        )
    )
    try:
        queued = run(effects.resolveAgentSpec("ctrl"))
        plain = run(effects.resolveAgentSpec("plain"))
    finally:
        effects._CTX = prev

    assert queued["subflowQueues"] == {"child": "fg"}
    assert plain["subflowQueues"] is None
