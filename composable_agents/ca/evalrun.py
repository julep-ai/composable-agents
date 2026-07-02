"""CLI/test-time runner for mem-mcp-style ``.ctx`` eval suites.

This module executes user-provided ``eval.py`` code with the same trust stance
as :func:`composable_agents.dotctx_evals.load_eval_module`: explicit eval entry
points only, never prompt loading. Tests inject a fake ``acompletion``; real CLI
runs resolve the provider completion lazily.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import os
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence

from composable_agents.agent_loop import AgentConfig, ROUND_NOTE_KEY, drive_agent_loop
from composable_agents.dotctx_evals import MockToolConfig, Sample, Turn, load_ctx_evals
from composable_agents.dotctx_rich import RichDotctx, load_rich_dotctx
from composable_agents.execution.llm import (
    AnyCompletion,
    _resolve_acompletion,
    complete_reasoner,
)
from composable_agents.registry import DEFAULT_REGISTRY, Registry


@dataclass(frozen=True)
class SampleScore:
    id: str
    score: float
    passed: bool

    def to_json(self) -> dict[str, Any]:
        return {"id": self.id, "score": self.score, "passed": self.passed}

    @staticmethod
    def from_json(d: dict[str, Any]) -> "SampleScore":
        return SampleScore(id=str(d["id"]), score=float(d["score"]), passed=bool(d["passed"]))


@dataclass(frozen=True)
class EvalReport:
    ctx: str
    model: str
    samples: int
    scores: tuple[SampleScore, ...]
    mean: float
    threshold: float
    passed: bool

    def to_json(self) -> dict[str, Any]:
        return {
            "ctx": self.ctx,
            "model": self.model,
            "samples": self.samples,
            "scores": [s.to_json() for s in self.scores],
            "mean": self.mean,
            "threshold": self.threshold,
            "passed": self.passed,
        }

    @staticmethod
    def from_json(d: dict[str, Any]) -> "EvalReport":
        return EvalReport(
            ctx=str(d["ctx"]),
            model=str(d["model"]),
            samples=int(d["samples"]),
            scores=tuple(SampleScore.from_json(s) for s in d["scores"]),
            mean=float(d["mean"]),
            threshold=float(d["threshold"]),
            passed=bool(d["passed"]),
        )


def _provider_tool_defs(expected: Mapping[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"type": "function", "function": {"name": key, "description": "", "parameters": schema}}
        for key, schema in expected.items()
    ]


def _resolve_mock(
    mock: Any,
    args: Any,
    counters: dict[str, int],
    key: str,
) -> Any:
    if isinstance(mock, MockToolConfig):
        margs = args if isinstance(args, dict) else {}
        for pattern, response in mock.match:
            if all(margs.get(k) == v for k, v in pattern.items()):
                return response
        if mock.responses:
            idx = counters.get(key, 0)
            counters[key] = idx + 1
            return mock.responses[idx % len(mock.responses)]
        return mock.default
    return mock


def _turn_from_reply(reply: Any) -> Turn:
    if isinstance(reply, dict) and isinstance(reply.get("tool_calls"), list):
        tool_calls = [
            {"name": tc.get("tool"), "args": tc.get("input")}
            for tc in reply["tool_calls"]
            if isinstance(tc, dict)
        ]
        return Turn(output=reply, tool_calls=tool_calls, tool_results=[], content=None, refusal=None)
    content = reply if isinstance(reply, str) else None
    return Turn(output=reply, tool_calls=[], tool_results=[], content=content, refusal=None)


async def _run_single_shot(
    reasoner: Any,
    sample: Sample,
    acompletion: AnyCompletion,
) -> Any:
    result = await complete_reasoner(reasoner, sample.input, acompletion=acompletion)
    reply = result.reply
    text = reply if isinstance(reply, str) else json.dumps(reply)
    return {"content": text}


async def _run_tool_loop(
    rich: RichDotctx,
    sample: Sample,
    acompletion: AnyCompletion,
) -> Any:
    reasoner = rich.reasoner
    tool_defs = _provider_tool_defs(rich.expected_tool_schemas)
    cfg = AgentConfig(
        max_rounds=reasoner.max_rounds or 24,
        native_tools=True,
        require_tool_call=reasoner.require_tool_call,
    )
    granted = set(reasoner.tools)
    mock_tools = sample.mock_tools or {}
    counters: dict[str, int] = {}

    async def call_tool(
        name: str,
        value: Any,
        *,
        call_index: Optional[int] = None,
    ) -> Any:
        del call_index
        if name not in mock_tools:
            raise KeyError(f"tool {name!r} was not mocked for this eval sample")
        return _resolve_mock(mock_tools[name], value, counters, name)

    stop_on = sample.stop_on
    turn_index = 0
    last_turn: Optional[Turn] = None

    async def invoke_controller(payload: dict[str, Any]) -> Any:
        nonlocal last_turn, turn_index
        if last_turn is not None and stop_on(last_turn, turn_index):
            return {"done": True, "output": last_turn.output}
        turn_index += 1
        value = dict(sample.input) if isinstance(sample.input, dict) else sample.input
        if isinstance(value, dict) and ROUND_NOTE_KEY in payload:
            value[ROUND_NOTE_KEY] = payload[ROUND_NOTE_KEY]
        result = await complete_reasoner(
            reasoner,
            value,
            acompletion=acompletion,
            tools=tool_defs,
            parallel_tool_calls=True,
        )
        last_turn = _turn_from_reply(result.reply)
        return result.reply

    return await drive_agent_loop(
        input=sample.input,
        cfg=cfg,
        invoke_controller=invoke_controller,
        call_tool=call_tool,
        granted=granted,
        contracts=None,
    )


async def run_eval(
    ctx_path: str,
    *,
    env_vars: Optional[Mapping[str, str]] = None,
    limit: Optional[int] = None,
    acompletion: Optional[AnyCompletion] = None,
    registry: Registry = DEFAULT_REGISTRY,
) -> EvalReport:
    env = dict(env_vars) if env_vars is not None else {}
    ctx = os.fspath(ctx_path)
    evals = load_ctx_evals(ctx, env=env)
    if evals.eval_module is None:
        raise ValueError(
            f"no eval.py in {ctx!r}: `ca eval` needs an eval.py exposing "
            "sample()/score() (see the mem-mcp eval surface)"
        )
    rich = load_rich_dotctx(ctx, registry=registry, env=env)
    module = evals.eval_module
    config = evals.eval_config
    threshold = config.threshold if config is not None else 0.5
    concurrency = config.concurrency if config is not None else 5
    reasoner = rich.reasoner
    resolved = _resolve_acompletion(acompletion)

    raw = module.sample(-1 if limit is None else limit)
    loaded_samples = await raw if inspect.isawaitable(raw) else raw
    samples: Sequence[Sample] = loaded_samples

    is_tool_loop = bool(reasoner.tools)
    sem = asyncio.Semaphore(max(1, concurrency))

    async def score_one(index: int, sample: Sample) -> SampleScore:
        async with sem:
            if is_tool_loop:
                output = await _run_tool_loop(rich, sample, resolved)
            else:
                output = await _run_single_shot(reasoner, sample, resolved)
            raw_score = module.score(sample.input, output, sample.expected)
            value = await raw_score if inspect.isawaitable(raw_score) else raw_score
            s = float(value)
            name = sample.name
            sid = name if name else f"sample-{index}"
            return SampleScore(id=sid, score=s, passed=s >= threshold)

    results = await asyncio.gather(*(score_one(i, s) for i, s in enumerate(samples)))
    mean = sum(r.score for r in results) / len(results) if results else 0.0
    return EvalReport(
        ctx=ctx,
        model=reasoner.model,
        samples=len(results),
        scores=tuple(results),
        mean=mean,
        threshold=threshold,
        passed=mean >= threshold,
    )


def run_eval_sync(
    ctx_path: str,
    *,
    env_vars: Optional[Mapping[str, str]] = None,
    limit: Optional[int] = None,
    acompletion: Optional[AnyCompletion] = None,
) -> EvalReport:
    return asyncio.run(run_eval(ctx_path, env_vars=env_vars, limit=limit, acompletion=acompletion))


def diff_reports(
    baseline: Mapping[str, Any],
    current: Mapping[str, Any],
    *,
    mean_tolerance: float = 0.01,
) -> tuple[list[str], bool]:
    base_by_id = {str(s["id"]): s for s in baseline.get("scores", []) if isinstance(s, dict)}
    regressed: list[str] = []
    for s in current.get("scores", []):
        if not isinstance(s, dict):
            continue
        sid = str(s["id"])
        b = base_by_id.get(sid)
        if b is not None and b.get("passed") and not s.get("passed"):
            regressed.append(sid)
    mean_regressed = (float(baseline.get("mean", 0.0)) - float(current.get("mean", 0.0))) > mean_tolerance
    return regressed, mean_regressed


__all__ = [
    "EvalReport",
    "SampleScore",
    "diff_reports",
    "run_eval",
    "run_eval_sync",
]
