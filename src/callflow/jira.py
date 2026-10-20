"""Create Jira issues for the items Rinvo's team must act on: bugs and agent configuration changes."""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping, MutableMapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from callflow.route import Inbox, RoutedMeeting
from callflow.schema import ActionItem
from callflow.verify import VerificationReport

JIRA_FILE = "jira.json"
JIRA_INBOXES = (Inbox.tickets, Inbox.config_changes)
LABELS = ["callflow"]
TIMEOUT_S = 30
SUMMARY_LIMIT = 255
ERROR_DETAIL_LIMIT = 500
UNVERIFIED_REASON = "evidence not verified in the transcript; needs human review"
REQUIRED_VARS = ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT_KEY")

Opener = Callable[..., Any]


class JiraError(RuntimeError):
    pass


@dataclass(frozen=True)
class JiraConfig:
    base_url: str
    email: str
    api_token: str = field(repr=False)
    project_key: str
    issue_type_bug: str = "Bug"
    issue_type_config: str = "Task"

    @classmethod
    def from_env(cls, environ: Mapping[str, str] = os.environ) -> JiraConfig:
        values = {name: environ.get(name, "").strip() for name in REQUIRED_VARS}
        missing = [name for name, value in values.items() if not value]
        if missing:
            names = ", ".join(missing)
            raise JiraError(f"missing Jira settings: {names} (set them in the environment or .env)")
        base_url = values["JIRA_BASE_URL"].rstrip("/")
        # Basic auth sends the token with every request, so never allow it over plain HTTP.
        if not base_url.startswith("https://"):
            raise JiraError("JIRA_BASE_URL must start with https://")
        return cls(
            base_url=base_url,
            email=values["JIRA_EMAIL"],
            api_token=values["JIRA_API_TOKEN"],
            project_key=values["JIRA_PROJECT_KEY"],
            issue_type_bug=environ.get("JIRA_ISSUE_TYPE_BUG", "").strip() or "Bug",
            issue_type_config=environ.get("JIRA_ISSUE_TYPE_CONFIG", "").strip() or "Task",
        )

    def auth_header(self) -> str:
        credentials = base64.b64encode(f"{self.email}:{self.api_token}".encode()).decode("ascii")
        return f"Basic {credentials}"

    def issue_type(self, inbox: Inbox) -> str:
        return self.issue_type_bug if inbox == Inbox.tickets else self.issue_type_config


@dataclass
class JiraPushResult:
    created: dict[str, str] = field(default_factory=dict)
    skipped: list[tuple[str, str]] = field(default_factory=list)


def load_dotenv(path: Path, environ: MutableMapping[str, str] = os.environ) -> None:
    """Read KEY=VALUE lines into the environment; variables that are already set win."""
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        line = line.removeprefix("export ").strip()
        key, separator, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if not separator or not key:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        environ.setdefault(key, value)


def push_to_jira(
    routed: RoutedMeeting,
    report: VerificationReport,
    out_dir: Path,
    config: JiraConfig,
    *,
    opener: Opener = urllib.request.urlopen,
) -> JiraPushResult:
    """Create one issue per verified bug/config item; items listed in jira.json are not created again."""
    mapping_path = out_dir / JIRA_FILE
    known = load_mapping(mapping_path)
    unverified = report.unverified_ids()
    result = JiraPushResult()
    for inbox in JIRA_INBOXES:
        for item in routed.inboxes.get(inbox, []):
            mapping_key = _mapping_key(item)
            if mapping_key in known:
                result.skipped.append((item.id, f"already in Jira as {known[mapping_key]}"))
            elif item.id in unverified:
                result.skipped.append((item.id, UNVERIFIED_REASON))
            else:
                payload = build_issue_payload(item, inbox, routed, report, config)
                key = create_issue(payload, config, opener)
                known[mapping_key] = key
                result.created[item.id] = key
                # Saved after every issue so a failure later in the run does not cause duplicates on retry.
                save_mapping(mapping_path, known)
    return result


def _mapping_key(item: ActionItem) -> str:
    # A fresh model run renumbers items, so the id alone could match a different item and silently
    # skip it; the title makes the key specific to this item.
    return f"{item.id} · {' '.join(item.title.split())}"


def build_issue_payload(
    item: ActionItem, inbox: Inbox, routed: RoutedMeeting, report: VerificationReport, config: JiraConfig
) -> dict:
    summary = " ".join(f"[{routed.extraction.client}] {item.title}".split())[:SUMMARY_LIMIT]
    fields: dict = {
        "project": {"key": config.project_key},
        "issuetype": {"name": config.issue_type(inbox)},
        "summary": summary,
        "description": build_description(item, routed, report),
        "labels": list(LABELS),
    }
    if item.due_date:
        fields["duedate"] = item.due_date.isoformat()
    return {"fields": fields}


def build_description(item: ActionItem, routed: RoutedMeeting, report: VerificationReport) -> str:
    facts = [
        ("Właściciel", item.owner),
        ("Termin", _due(item)),
        ("Warunek", item.condition),
        ("Ograniczenia", "; ".join(item.constraints)),
        ("Zatwierdza", item.approval_by),
        ("Wersja ostateczna", item.final_value),
        ("Zastępuje", "; ".join(item.superseded)),
        ("Zależy od", ", ".join(item.depends_on)),
    ]
    lines = [item.details, ""]
    lines += [f"{label}: {value}" for label, value in facts if value]
    quotes = [f"{check.speaker} (l. {check.line}): „{check.quote}”" for check in report.quotes_for(item.id)]
    if quotes:
        lines += ["", "Cytaty z rozmowy:", *quotes]
    meeting_date = routed.extraction.meeting_date or "nieznana data"
    lines += [
        "",
        f"Pozycja {item.id}. Utworzone automatycznie przez callflow z rozmowy z {meeting_date}",
    ]
    return "\n".join(lines)


def _due(item: ActionItem) -> str | None:
    if item.due_date and item.due_text:
        return f"{item.due_date} („{item.due_text}”)"
    if item.due_date:
        return str(item.due_date)
    return f"bez daty („{item.due_text}”)" if item.due_text else None


def create_issue(payload: dict, config: JiraConfig, opener: Opener) -> str:
    """POST /rest/api/2/issue (v2 takes a plain-text description; v3 would require ADF)."""
    request = urllib.request.Request(
        f"{config.base_url}/rest/api/2/issue",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": config.auth_header(),
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with opener(request, timeout=TIMEOUT_S) as response:
            body = response.read()
    except urllib.error.HTTPError as exc:
        detail = _redact(_error_detail(exc), config)
        raise JiraError(f"Jira rejected the issue (HTTP {exc.code}): {detail}") from None
    except OSError as exc:  # URLError, timeouts and dropped connections
        reason = getattr(exc, "reason", exc)
        raise JiraError(f"cannot reach Jira at {config.base_url}: {reason}") from None
    try:
        return json.loads(body)["key"]
    except (ValueError, KeyError, TypeError):
        raise JiraError(f"unexpected response from Jira: {body[:ERROR_DETAIL_LIMIT]!r}") from None


def _error_detail(exc: urllib.error.HTTPError) -> str:
    try:
        text = exc.read().decode("utf-8", errors="replace")
    except OSError:
        return exc.reason or "no details"
    try:
        data = json.loads(text)
        messages = list(data.get("errorMessages") or [])
        messages += [f"{name}: {message}" for name, message in (data.get("errors") or {}).items()]
        text = "; ".join(messages) or text
    except (ValueError, AttributeError):
        pass
    return text[:ERROR_DETAIL_LIMIT] or (exc.reason or "no details")


def _redact(text: str, config: JiraConfig) -> str:
    return text.replace(config.api_token, "***") if config.api_token else text


def load_mapping(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise JiraError(f"{path} is not valid JSON ({exc}); fix or remove it") from None
    if not isinstance(data, dict) or not all(isinstance(v, str) for v in data.values()):
        raise JiraError(f"{path} must map item ids to Jira issue keys")
    return data


def save_mapping(path: Path, mapping: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
