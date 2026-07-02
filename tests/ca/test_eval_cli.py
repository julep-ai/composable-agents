from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import pytest

pytest.importorskip("jinja2")
pytest.importorskip("yglu")  # the vendored .ctx settings carry `!?` env expressions

from composable_agents.ca import cli
from composable_agents.ca.evalrun import EvalReport, diff_reports, run_eval, run_eval_sync
from composable_agents.dotctx import load_dotctx
from conftest import run


@dataclass
class FakeMessage:
    content: Optional[str] = None
    parsed: Any = None
    tool_calls: Any = None


@dataclass
class FakeChoice:
    message: FakeMessage


@dataclass
class FakeCompletion:
    choices: list[FakeChoice]


@dataclass
class FakeFunction:
    name: str
    arguments: str


@dataclass
class FakeToolCall:
    id: str
    function: FakeFunction


def _content(text: str) -> FakeCompletion:
    return FakeCompletion(choices=[FakeChoice(FakeMessage(content=text))])


def _parsed(obj: Any) -> FakeCompletion:
    return FakeCompletion(choices=[FakeChoice(FakeMessage(parsed=obj))])


def _tool_call_completion(id: str, name: str, args_json: str) -> FakeCompletion:
    return FakeCompletion(
        choices=[
            FakeChoice(
                FakeMessage(
                    tool_calls=[FakeToolCall(id, FakeFunction(name, args_json))]
                )
            )
        ]
    )


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "memmcp"


def _good_summary_json() -> str:
    return json.dumps(
        {
            "summary": (
                "Alice met Bob in London about the Atlas rollout. "
                "Nina approved Atlas in Berlin."
            )
        }
    )


class SingleShotFake:
    def __init__(self, content: str, delay: float = 0.0):
        self.content = content
        self.delay = delay
        self.in_flight = 0
        self.max_in_flight = 0
        self.calls = 0

    async def __call__(self, **kwargs):
        self.calls += 1
        self.in_flight += 1
        self.max_in_flight = max(self.max_in_flight, self.in_flight)
        try:
            if self.delay:
                await asyncio.sleep(self.delay)
            return _content(self.content)
        finally:
            self.in_flight -= 1


class ToolLoopFake:
    def __init__(self, tool_name: str, tool_args_json: str):
        self.tool_name = tool_name
        self.tool_args_json = tool_args_json
        self._seen: dict[str, int] = {}

    async def __call__(self, **kwargs):
        key = json.dumps(kwargs["messages"], sort_keys=True, default=str)
        n = self._seen.get(key, 0)
        self._seen[key] = n + 1
        if n == 0:
            return _tool_call_completion("c1", self.tool_name, self.tool_args_json)
        return _parsed({"done": True})


def test_single_shot_report_shape_and_pass() -> None:
    report = run(
        run_eval(
            str(FIXTURES / "episode_summary.ctx"),
            acompletion=SingleShotFake(_good_summary_json()),
        )
    )

    data = report.to_json()
    assert set(data) == {"ctx", "model", "samples", "scores", "mean", "threshold", "passed"}
    assert data == EvalReport.from_json(data).to_json()
    assert report.samples == 2
    assert all(set(score) == {"id", "score", "passed"} for score in data["scores"])
    assert [score.id for score in report.scores] == ["meeting_with_context", "empty_background"]
    assert report.threshold == 0.5
    assert report.mean == 1.0
    assert report.passed is True
    assert report.model == load_dotctx(str(FIXTURES / "episode_summary.ctx"), env={}).model


def test_single_shot_below_threshold() -> None:
    report = run(
        run_eval(
            str(FIXTURES / "episode_summary.ctx"),
            acompletion=SingleShotFake("not json"),
        )
    )

    assert [score.score for score in report.scores] == [0.0, 0.0]
    assert report.mean == 0.0
    assert report.passed is False


def test_tool_loop_scores_trace_derived_output() -> None:
    report = run(
        run_eval(
            str(FIXTURES / "execute_eval.ctx"),
            acompletion=ToolLoopFake("record_memory", '{"content": "hi"}'),
            limit=1,
        )
    )

    reasoner = load_dotctx(str(FIXTURES / "execute_eval.ctx"), env={})
    assert bool(reasoner.tools) is True
    assert report.samples == 1
    assert report.scores[0].id == "records_ok"
    assert report.scores[0].score == 1.0
    assert report.scores[0].passed is True


def test_tool_loop_unmocked_tool_scored_failure() -> None:
    report = run(
        run_eval(
            str(FIXTURES / "execute_eval.ctx"),
            acompletion=ToolLoopFake("record_memory", '{"content":"x"}'),
            limit=None,
        )
    )

    by_id = {score.id: score for score in report.scores}
    assert by_id["records_ok"].score == 1.0
    assert by_id["records_ok"].passed is True
    assert by_id["unmocked_fails"].score == 0.0
    assert by_id["unmocked_fails"].passed is False


def test_baseline_regression_exit_via_diff_reports() -> None:
    good = run(
        run_eval(
            str(FIXTURES / "episode_summary.ctx"),
            acompletion=SingleShotFake(_good_summary_json()),
        )
    )
    bad = run(
        run_eval(
            str(FIXTURES / "episode_summary.ctx"),
            acompletion=SingleShotFake("not json"),
        )
    )

    regressed_ids, mean_regressed = diff_reports(good.to_json(), bad.to_json())
    assert set(regressed_ids) == {"meeting_with_context", "empty_background"}
    assert mean_regressed is True
    assert diff_reports(good.to_json(), good.to_json()) == ([], False)


def test_concurrency_bounded(tmp_path: Path) -> None:
    ctx = tmp_path / "parallel.ctx"
    ctx.mkdir()
    (ctx / "settings.yaml").write_text(
        'model: "openai/gpt-eval@low"\n',
        encoding="utf-8",
    )
    (ctx / "prompt.j2").write_text(
        "<<< role:system >>>\n"
        "Reply with JSON.\n\n"
        "<<< role:user >>>\n"
        'Task: {{ task | default("", true) }}\n',
        encoding="utf-8",
    )
    (ctx / "eval.yaml").write_text(
        "threshold: 0.0\n"
        "concurrency: 2\n\n"
        "datasets:\n"
        "  - file: eval.py\n"
        "    format: py\n",
        encoding="utf-8",
    )
    (ctx / "eval.py").write_text(
        "from dotctx.eval_types import Sample\n\n"
        "def sample(limit: int = -1):\n"
        "    samples = [\n"
        "        Sample(name=f's{i}', input={'task': f'task-{i}'})\n"
        "        for i in range(6)\n"
        "    ]\n"
        "    return samples if limit is None or limit < 0 else samples[:limit]\n\n"
        "def score(_input, output, expected):\n"
        "    return 1.0\n",
        encoding="utf-8",
    )
    fake = SingleShotFake(content='{"ok": 1}', delay=0.02)

    report = run(run_eval(str(ctx), acompletion=fake))

    assert fake.max_in_flight <= 2
    assert report.samples == 6


def test_cli_exit_codes(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        "composable_agents.ca.evalrun._resolve_acompletion",
        lambda a: SingleShotFake(_good_summary_json()),
    )
    assert cli.main(["eval", str(FIXTURES / "episode_summary.ctx")]) == 0

    json_path = tmp_path / "report.json"
    assert cli.main(["eval", str(FIXTURES / "episode_summary.ctx"), "--json", str(json_path)]) == 0
    assert set(json.loads(json_path.read_text(encoding="utf-8"))) == {
        "ctx",
        "model",
        "samples",
        "scores",
        "mean",
        "threshold",
        "passed",
    }

    good = run(
        run_eval(
            str(FIXTURES / "episode_summary.ctx"),
            acompletion=SingleShotFake(_good_summary_json()),
        )
    )
    baseline_path = tmp_path / "baseline.json"
    baseline_path.write_text(json.dumps(good.to_json()), encoding="utf-8")

    monkeypatch.setattr(
        "composable_agents.ca.evalrun._resolve_acompletion",
        lambda a: SingleShotFake("not json"),
    )
    assert cli.main(["eval", str(FIXTURES / "episode_summary.ctx")]) == 2
    assert (
        cli.main(
            [
                "eval",
                str(FIXTURES / "episode_summary.ctx"),
                "--baseline",
                str(baseline_path),
            ]
        )
        == 3
    )


def test_missing_eval_py_is_teaching_error() -> None:
    with pytest.raises(ValueError, match="eval.py"):
        run_eval_sync(str(FIXTURES / "cluster_label.ctx"))

    assert cli.main(["eval", str(FIXTURES / "cluster_label.ctx")]) == 2
