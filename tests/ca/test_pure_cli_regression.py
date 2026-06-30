from pathlib import Path

import pytest

# A flow that uses a @pure. The pure body is echo-tolerant: it reads only
# dict.keys(), so it never KeyErrors under ca run's {"output": value} echo stubs.
PURE_SAMPLE = '''
from composable_agents import flow, pure, think, tool

@tool(effect="read", idempotent=True)
def lookup(ticket: str) -> dict:
    return {"queue": "billing"}

@pure("passthrough")
def passthrough(hit: dict) -> dict:
    return {"seen": sorted(hit.keys())}

@flow
def triage(ticket: str) -> dict:
    hit = lookup(ticket)
    prompt = passthrough(hit)
    answer = think("reply", prompt)
    return prompt | answer
'''


@pytest.fixture
def pure_module(tmp_path: Path) -> Path:
    """A ca project whose only agent uses a @pure (the case the suite never covered)."""
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "agents.py").write_text(PURE_SAMPLE, encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text('[tool.ca]\nsrc = ["pkg"]\n', encoding="utf-8")
    return tmp_path


def test_lint_resolves_pures_no_unknown_pure(pure_module: Path) -> None:
    from composable_agents.ca.config import load_config
    from composable_agents.ca.lint import lint_agents

    cfg = load_config(pure_module)
    findings, exit_code = lint_agents(cfg, ["triage"], fail_severity="error")
    codes = [f.code for f in findings]
    assert "UNKNOWN_PURE" not in codes, f"pure not resolved by ca lint: {findings}"
    assert "RESOLVE" not in codes, f"resolve failed: {findings}"
    assert exit_code == 0
