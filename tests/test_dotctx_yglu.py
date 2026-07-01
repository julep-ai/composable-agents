"""Task 7: yglu-evaluated settings.yaml with an explicit $env binding.

The first group of tests exercises real yglu evaluation and skips without the
[yglu] extra (per-test importorskip). The hard-error test runs everywhere —
it is exactly the no-yglu path.
"""
import os

import pytest

from composable_agents.dotctx import load_dotctx
from composable_agents.dotctx_yglu import has_yglu_tags, load_settings

SETTINGS = 'model: !? $env.get("SUMMARY_MODEL", "openai/gpt-5.4-nano@medium")\n'


def test_has_yglu_tags() -> None:
    assert has_yglu_tags(SETTINGS)
    assert not has_yglu_tags("model: openai:gpt-4o\n")


def test_env_default_when_unset() -> None:
    pytest.importorskip("yglu")
    out = load_settings(SETTINGS, env={}, filepath="settings.yaml")
    assert out["model"] == "openai/gpt-5.4-nano@medium"


def test_explicit_env_wins_and_ambient_never_leaks() -> None:
    pytest.importorskip("yglu")
    os.environ["SUMMARY_MODEL"] = "ambient:leak"
    try:
        out = load_settings(SETTINGS, env={"SUMMARY_MODEL": "openai:gpt-5.5@low"},
                            filepath="settings.yaml")
        assert out["model"] == "openai:gpt-5.5@low"
        out2 = load_settings(SETTINGS, env={}, filepath="settings.yaml")
        assert out2["model"] == "openai/gpt-5.4-nano@medium"   # ambient invisible
    finally:
        del os.environ["SUMMARY_MODEL"]


def test_load_dotctx_end_to_end(tmp_path) -> None:
    pytest.importorskip("yglu")
    d = tmp_path / "summary.ctx"
    d.mkdir()
    (d / "settings.yaml").write_text(SETTINGS)
    r = load_dotctx(str(d), env={"SUMMARY_MODEL": "anthropic:claude-sonnet-4-6@high"})
    assert r.model == "anthropic:claude-sonnet-4-6"
    assert r.reasoning_effort == "high"


def test_tagged_settings_without_yglu_is_hard_error(tmp_path, monkeypatch) -> None:
    import composable_agents.dotctx_yglu as dy
    monkeypatch.setattr(dy, "_import_yglu", lambda: (_ for _ in ()).throw(
        ImportError("no yglu")))
    d = tmp_path / "t.ctx"
    d.mkdir()
    (d / "settings.yaml").write_text(SETTINGS)
    with pytest.raises(ImportError, match=r"composable-agents\[yglu\]"):
        load_dotctx(str(d))
