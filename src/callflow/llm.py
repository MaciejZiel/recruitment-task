"""Structured-output calls to Claude through the Claude Code CLI (`claude -p`).

The CLI is used instead of the Anthropic SDK because it runs on the local Claude Code login, so no API
key is needed. Any other backend only has to provide the same `complete_json` signature.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_MODEL = "claude-opus-5-5"
DEFAULT_EFFORT = "high"
DEFAULT_TIMEOUT_S = 900


class LLMError(RuntimeError):
    pass


@dataclass
class LLMResponse:
    data: dict[str, Any]
    raw: dict[str, Any]


def find_claude_executable() -> str:
    found = shutil.which("claude")
    if found is None:
        raise LLMError(
            "Claude Code CLI ('claude') not found in PATH. Install and log in to Claude Code, "
            "or render an existing result with --from-json."
        )
    path = Path(found)
    if path.suffix.lower() not in {".cmd", ".bat"}:
        return found
    # On Windows npm installs a .cmd shim; arguments passed through cmd.exe get mangled (quotes,
    # newlines in the prompt and JSON schema), so call the native binary the shim points to.
    native = path.parent / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
    if not native.is_file():
        raise LLMError(f"Found the npm shim {path}, but not the native binary at {native}.")
    return str(native)


def complete_json(
    system: str,
    user: str,
    schema: dict[str, Any],
    *,
    model: str = DEFAULT_MODEL,
    effort: str = DEFAULT_EFFORT,
    timeout_s: int = DEFAULT_TIMEOUT_S,
) -> LLMResponse:
    executable = find_claude_executable()
    command = [
        executable,
        "-p",
        "--system-prompt",
        system,
        "--json-schema",
        json.dumps(schema, ensure_ascii=False, separators=(",", ":")),
        "--output-format",
        "json",
        "--model",
        model,
        "--effort",
        effort,
        # Isolate the call: no tools, MCP servers, user/project settings or saved session.
        "--tools",
        "",
        "--strict-mcp-config",
        "--setting-sources",
        "",
        "--no-session-persistence",
    ]
    try:
        completed = subprocess.run(
            command, input=user.encode("utf-8"), capture_output=True, timeout=timeout_s, check=False
        )
    except subprocess.TimeoutExpired as exc:
        raise LLMError(f"claude -p did not finish within {timeout_s} s") from exc

    stdout = completed.stdout.decode("utf-8", errors="replace")
    stderr = completed.stderr.decode("utf-8", errors="replace").strip()
    try:
        raw = json.loads(stdout)
    except json.JSONDecodeError as exc:
        detail = stderr or stdout[:500] or "no output"
        raise LLMError(f"claude -p exited with code {completed.returncode}: {detail}") from exc

    if completed.returncode != 0 or raw.get("is_error"):
        detail = raw.get("result") or raw.get("subtype") or stderr or "unknown error"
        raise LLMError(f"claude -p failed (exit code {completed.returncode}): {detail}")

    data = raw.get("structured_output")
    if not isinstance(data, dict):
        raise LLMError(f"claude -p returned no structured output (stop: {raw.get('stop_reason')})")
    return LLMResponse(data=data, raw=raw)
