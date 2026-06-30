from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any

from composable_agents.ca._echo import build_echo_env
from composable_agents.ca.resolve import ResolvedAgent
from composable_agents.execution.interpreter import interpret
from composable_agents.ir import Node
from composable_agents.projection import ProjectionEvent


@dataclass(frozen=True)
class RunOutcome:
    run_id: str
    value: Any
    events: list[ProjectionEvent] = field(default_factory=list)
    error: str | None = None


def run_agent_local(resolved: ResolvedAgent, value: Any, *, run_id: str) -> RunOutcome:
    if resolved.error is not None:
        return RunOutcome(run_id=run_id, value=None, events=[], error=resolved.error)
    projection = None
    try:
        node = Node.from_json(resolved.ir)
        env, projection = build_echo_env(node)
        result = asyncio.run(interpret(node, value, env))
    except Exception as exc:  # noqa: BLE001 - surface runtime errors in the outcome.
        events = projection.events() if projection is not None else []
        return RunOutcome(run_id=run_id, value=None, events=events, error=str(exc))
    return RunOutcome(run_id=run_id, value=result.value, events=projection.events(), error=None)
