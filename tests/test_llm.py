import json
import subprocess
from pathlib import Path

import pytest

from callflow import llm


def test_missing_cli_gives_actionable_error(monkeypatch):
    monkeypatch.setattr(llm.shutil, "which", lambda name: None)
    with pytest.raises(llm.LLMError, match="--from-json"):
        llm.find_claude_executable()


def test_npm_cmd_shim_resolves_to_native_binary(monkeypatch, tmp_path: Path):
    shim = tmp_path / "claude.CMD"
    shim.write_text("@echo off", encoding="utf-8")
    native = tmp_path / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
    native.parent.mkdir(parents=True)
    native.write_bytes(b"")
    monkeypatch.setattr(llm.shutil, "which", lambda name: str(shim))

    assert llm.find_claude_executable() == str(native)


def test_non_shim_executable_is_used_directly(monkeypatch):
    monkeypatch.setattr(llm.shutil, "which", lambda name: "/usr/local/bin/claude")
    assert llm.find_claude_executable() == "/usr/local/bin/claude"


def run_with(monkeypatch, *, stdout=b"", stderr=b"", returncode=0, raises=None):
    seen = {}

    def fake_run(command, **kwargs):
        seen["command"], seen["input"] = command, kwargs["input"]
        if raises:
            raise raises
        return subprocess.CompletedProcess(command, returncode, stdout, stderr)

    monkeypatch.setattr(llm, "find_claude_executable", lambda: "claude")
    monkeypatch.setattr(llm.subprocess, "run", fake_run)
    return seen


def test_structured_output_is_returned_and_input_goes_via_stdin(monkeypatch):
    seen = run_with(
        monkeypatch, stdout=json.dumps({"structured_output": {"a": 1}, "is_error": False}).encode()
    )

    response = llm.complete_json("system", "dane: zażółć", {"type": "object"})

    assert response.data == {"a": 1}
    assert seen["input"] == "dane: zażółć".encode()
    assert seen["command"][seen["command"].index("--json-schema") + 1] == '{"type":"object"}'
    assert seen["command"][seen["command"].index("--tools") + 1] == ""


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"stdout": b"not json", "returncode": 1, "stderr": b"auth failed"}, "auth failed"),
        ({"stdout": b"[]"}, "unexpected JSON"),
        ({"stdout": json.dumps({"is_error": True, "result": "quota"}).encode()}, "quota"),
        ({"stdout": json.dumps({"is_error": False, "stop_reason": "max_tokens"}).encode()}, "max_tokens"),
        ({"raises": subprocess.TimeoutExpired("claude", 1)}, "did not finish"),
    ],
)
def test_failures_become_llm_errors(monkeypatch, kwargs, message):
    run_with(monkeypatch, **kwargs)
    with pytest.raises(llm.LLMError, match=message):
        llm.complete_json("s", "u", {})
