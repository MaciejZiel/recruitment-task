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
