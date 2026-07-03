"""Wire-path decision (spike, any-llm-sdk 1.19.0, live Anthropic, 2026-07-02):
Production uses **acompletion + a block-form system message carrying
`cache_control`** (path a). Proven: two identical live `acompletion` calls with
a `{"role":"system","content":[{"type":"text","text":...,"cache_control":
{"type":"ephemeral","ttl":"1h"}}]}` message — call 1 reported
`usage.prompt_tokens=6453`, `usage.prompt_tokens_details.cached_tokens=None`
(cache create), call 2 reported `cached_tokens=6441` (cache read hit).
any-llm's anthropic *completion* adapter (`providers/anthropic/utils.py`) (1)
string-concatenates multiple system messages via `system_message += "\n" + ...`
— so a list-content system block collides/crashes when >1 system message is
present; the seam therefore MERGES all system messages into exactly one
block-form system message; (2) passes non-image/file content blocks through
unchanged, so `cache_control` on a message content block survives; (3) in
`_convert_response`, surfaces cache READ as
`usage.prompt_tokens_details.cached_tokens` but FOLDS cache creation into
`prompt_tokens` (no separate field) — so on the acompletion path
`cache_read_tokens` is observable and `cache_creation_tokens` is None. The
native `amessages` API (path b) surfaces both raw
`cache_creation_input_tokens`/`cache_read_input_tokens` but returns a native
`MessageResponse` (not an OpenAI ChatCompletion) that would not compose with
CA's parsing/resilience ladder — rejected for production, used only to
cross-check the spike.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Optional

import pytest

from composable_agents.deploy import _reasoner_identity
from composable_agents.dotctx import Reasoner, reasoner_from_settings
from composable_agents.execution.llm import (
    _apply_prompt_cache,
    _messages,
    complete_reasoner,
    make_resilient_llm_caller,
)
from composable_agents.execution.llm_result import LlmCallMeta
from composable_agents.registry import DEFAULT_REGISTRY
from composable_agents.resilience import ErrorClass, ResiliencePolicy
from conftest import run


@dataclass
class FakePromptTokensDetails:
    cached_tokens: int | None = None


@dataclass
class FakeUsage:
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    cache_read_input_tokens: int | None = None
    cache_creation_input_tokens: int | None = None
    prompt_tokens_details: FakePromptTokensDetails | None = None


@dataclass
class FakeMessage:
    content: Optional[str] = None
    parsed: Any = None


@dataclass
class FakeChoice:
    message: FakeMessage


@dataclass
class FakeCompletion:
    choices: list[FakeChoice]
    usage: FakeUsage | None = None
    model: str | None = None


def _completion(content: Optional[str] = "ok", usage: FakeUsage | None = None) -> FakeCompletion:
    return FakeCompletion(choices=[FakeChoice(FakeMessage(content=content))], usage=usage)


@dataclass
class Recorder:
    """An ``acompletion`` stand-in that records kwargs and replays a script."""

    replies: list[Any]
    calls: list[dict[str, Any]] = field(default_factory=list)
    _i: int = 0

    async def __call__(self, **kwargs: Any) -> FakeCompletion:
        self.calls.append(kwargs)
        reply = self.replies[self._i]
        self._i += 1
        if isinstance(reply, Exception):
            raise reply
        assert isinstance(reply, FakeCompletion)
        return reply


def _one_system(messages: list[dict[str, Any]]) -> dict[str, Any]:
    system = [m for m in messages if m.get("role") == "system"]
    assert len(system) == 1
    return system[0]


def test_anthropic_1h_block_system_and_tail_marker() -> None:
    rec = Recorder([_completion()])
    reasoner = Reasoner(
        name="pc1",
        model="anthropic:claude-x",
        system="stable system",
        prompt_cache="1h",
    )
    transcript = [{"role": "assistant", "content": "previous answer"}]

    run(complete_reasoner(reasoner, "next question", acompletion=rec, transcript=transcript))

    sent = rec.calls[0]["messages"]
    system = _one_system(sent)
    cc = {"type": "ephemeral", "ttl": "1h"}
    assert system["content"] == [
        {"type": "text", "text": "stable system", "cache_control": cc}
    ]
    assert sent[-1]["role"] == "user"
    assert sent[-1]["content"] == [
        {"type": "text", "text": "next question", "cache_control": cc}
    ]


def test_5m_omits_ttl() -> None:
    rec = Recorder([_completion()])
    reasoner = Reasoner(
        name="pc5m",
        model="anthropic:claude-x",
        system="stable system",
        prompt_cache="5m",
    )

    run(complete_reasoner(reasoner, "next question", acompletion=rec))

    system = _one_system(rec.calls[0]["messages"])
    assert system["content"][0]["cache_control"] == {"type": "ephemeral"}


def test_unset_prompt_cache_plain_strings_golden() -> None:
    rec = Recorder([_completion()])
    reasoner = Reasoner(name="pcunset", model="anthropic:claude-x", system="stable system")
    transcript = [{"role": "assistant", "content": "previous answer"}]

    run(complete_reasoner(reasoner, "next question", acompletion=rec, transcript=transcript))

    expected = _messages(
        "stable system",
        "next question",
        schema_hint=None,
        transcript=transcript,
    )
    assert rec.calls[0]["messages"] == expected
    assert isinstance(rec.calls[0]["messages"][0]["content"], str)
    assert isinstance(rec.calls[0]["messages"][-1]["content"], str)


def test_openai_set_is_inert_but_recorded() -> None:
    rec = Recorder([_completion()])
    reasoner = Reasoner(
        name="pcopenai",
        model="openai:gpt-4o",
        system="stable system",
        prompt_cache="1h",
    )

    result = run(complete_reasoner(reasoner, "next question", acompletion=rec))

    assert rec.calls[0]["messages"] == _messages(
        "stable system",
        "next question",
        schema_hint=None,
    )
    assert isinstance(rec.calls[0]["messages"][0]["content"], str)
    assert isinstance(rec.calls[0]["messages"][-1]["content"], str)
    assert result.meta.prompt_cache_requested == "1h"
    assert result.meta.prompt_cache_applied is False
    assert result.meta.prompt_cache_reason == "provider_inert"


def test_anthropic_meta_applied() -> None:
    rec = Recorder([_completion()])
    reasoner = Reasoner(
        name="pcmeta",
        model="anthropic:claude-x",
        system="stable system",
        prompt_cache="1h",
    )

    result = run(complete_reasoner(reasoner, "next question", acompletion=rec))

    assert result.meta.prompt_cache_requested == "1h"
    assert result.meta.prompt_cache_applied is True
    assert result.meta.prompt_cache_reason is None


def test_fallback_crossing_provider_records_reason() -> None:
    script = Recorder([TimeoutError("slow"), _completion("fine")])

    async def no_sleep(_seconds: float) -> None:
        return None

    caller = make_resilient_llm_caller(
        policy=ResiliencePolicy(
            fallbacks={"anthropic:claude-x": ["openai:gpt-4o"]},
            timeout_attempts=1,
        ),
        classifier=lambda exc: ErrorClass.TIMEOUT,
        sleep=no_sleep,
        acompletion=script,
    )
    reasoner = Reasoner(
        name="pcfallback",
        model="anthropic:claude-x",
        system="stable system",
        prompt_cache="1h",
    )

    result = run(caller(reasoner, "next question"))

    assert result.meta.prompt_cache_reason == "fallback_provider"
    assert result.meta.prompt_cache_applied is False


def test_meta_cache_tokens_from_usage() -> None:
    rec = Recorder(
        [
            _completion(
                usage=FakeUsage(
                    prompt_tokens=10,
                    completion_tokens=2,
                    total_tokens=12,
                    cache_read_input_tokens=100,
                    cache_creation_input_tokens=40,
                )
            )
        ]
    )
    reasoner = Reasoner(
        name="pccacheusage",
        model="anthropic:claude-x",
        system="stable system",
        prompt_cache="1h",
    )

    result = run(complete_reasoner(reasoner, "next question", acompletion=rec))

    assert result.meta.cache_read_tokens == 100
    assert result.meta.cache_creation_tokens == 40


def test_meta_cache_tokens_from_prompt_tokens_details() -> None:
    rec = Recorder(
        [
            _completion(
                usage=FakeUsage(
                    prompt_tokens=10,
                    completion_tokens=2,
                    total_tokens=12,
                    prompt_tokens_details=FakePromptTokensDetails(cached_tokens=77),
                )
            )
        ]
    )
    reasoner = Reasoner(
        name="pccachedetails",
        model="anthropic:claude-x",
        system="stable system",
        prompt_cache="1h",
    )

    result = run(complete_reasoner(reasoner, "next question", acompletion=rec))

    assert result.meta.cache_read_tokens == 77
    assert result.meta.cache_creation_tokens is None


def test_to_attrs_omits_cache_when_unset() -> None:
    meta = LlmCallMeta(served_model="gpt-4o", provider="openai")

    assert "llm.cache" not in meta.to_attrs()


def test_to_attrs_emits_cache_dict() -> None:
    meta = LlmCallMeta(
        served_model="claude-x",
        provider="anthropic",
        prompt_cache_requested="1h",
        prompt_cache_applied=True,
        cache_read_tokens=5,
    )

    assert meta.to_attrs()["llm.cache"] == {
        "requested": "1h",
        "applied": True,
        "read": 5,
    }


def test_settings_loader_accepts_and_validates() -> None:
    assert reasoner_from_settings(
        {"name": "pcsettings1", "model": "anthropic:claude-x", "prompt_cache": "1h"}
    ).prompt_cache == "1h"
    assert reasoner_from_settings(
        {"name": "pcsettings5", "model": "anthropic:claude-x", "promptCache": "5m"}
    ).prompt_cache == "5m"

    with pytest.raises(ValueError, match="5m.*1h|1h.*5m"):
        reasoner_from_settings(
            {"name": "pcsettingsbad", "model": "anthropic:claude-x", "prompt_cache": "2h"}
        )


def test_deploy_identity_omits_when_unset() -> None:
    DEFAULT_REGISTRY.register_reasoner(
        Reasoner(name="pcidentunset", model="anthropic:claude-x", system="stable system")
    )
    DEFAULT_REGISTRY.register_reasoner(
        Reasoner(
            name="pcidentset",
            model="anthropic:claude-x",
            system="stable system",
            prompt_cache="1h",
        )
    )

    assert "promptCache" not in _reasoner_identity("pcidentunset")
    assert _reasoner_identity("pcidentset")["promptCache"] == "1h"


def test_phase3_transcript_toolcall_collision_regression() -> None:
    cc = {"type": "ephemeral", "ttl": "1h"}
    tool_calls = [
        {
            "id": "call-1",
            "type": "function",
            "function": {"name": "lookup", "arguments": "{\"q\":\"x\"}"},
        }
    ]
    assistant = {"role": "assistant", "content": None, "tool_calls": tool_calls}
    tool = {"role": "tool", "tool_call_id": "call-1", "content": "tool result"}
    messages = [
        {"role": "system", "content": "leading system"},
        {"role": "system", "content": "[older turns elided]"},
        assistant,
        tool,
        {"role": "user", "content": "final question"},
        {"role": "system", "content": "round note"},
    ]

    out, _ = _apply_prompt_cache("anthropic", "1h", messages, {})

    system = _one_system(out)
    assert isinstance(system["content"], list)
    assert system["content"][0] == {
        "type": "text",
        "text": "leading system\n[older turns elided]",
        "cache_control": cc,
    }
    assert system["content"][1] == {"type": "text", "text": "round note"}
    assert not any(
        m.get("role") == "system" and isinstance(m.get("content"), str) for m in out
    )
    assert next(m for m in out if m.get("role") == "assistant") == assistant
    assert next(m for m in out if m.get("role") == "tool") == tool
    user = next(m for m in out if m.get("role") == "user")
    assert user["content"] == [
        {"type": "text", "text": "final question", "cache_control": cc}
    ]


@pytest.mark.live
@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY is required for the live Anthropic cache spike",
)
def test_live_anthropic_cache_create_then_read() -> None:
    from any_llm import acompletion

    stable_text = " ".join(f"cache-token-{i}" for i in range(2500))
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": stable_text,
                    "cache_control": {"type": "ephemeral", "ttl": "1h"},
                }
            ],
        },
        {"role": "user", "content": "Reply with exactly: ok"},
    ]

    async def call_twice() -> Any:
        await acompletion(
            provider="anthropic",
            model="claude-haiku-4-5-20251001",
            messages=messages,
            max_tokens=8,
        )
        return await acompletion(
            provider="anthropic",
            model="claude-haiku-4-5-20251001",
            messages=messages,
            max_tokens=8,
        )

    completion = run(call_twice())
    details = completion.usage.prompt_tokens_details
    assert isinstance(details.cached_tokens, int)
    assert details.cached_tokens > 0
