import base64
import io
import json
import urllib.error
from datetime import date
from email.message import Message

import pytest
from conftest import make_extraction, make_item

from callflow.jira import JIRA_FILE, JiraConfig, JiraError, load_dotenv, push_to_jira
from callflow.route import route
from callflow.schema import Evidence, Kind, State
from callflow.verify import verify

TOKEN = "secret-token-123"
ENV = {
    "JIRA_BASE_URL": "https://example.atlassian.net/",
    "JIRA_EMAIL": "bot@example.com",
    "JIRA_API_TOKEN": TOKEN,
    "JIRA_PROJECT_KEY": "RIN",
}


class FakeJira:
    """Stands in for urllib.request.urlopen and records every request."""

    def __init__(self, fail_with: Exception | None = None):
        self.requests = []
        self.fail_with = fail_with

    def __call__(self, request, timeout):
        self.requests.append((request, timeout))
        if self.fail_with:
            raise self.fail_with
        return io.BytesIO(json.dumps({"id": "1", "key": f"RIN-{len(self.requests)}"}).encode())

    def payloads(self):
        return [json.loads(request.data) for request, _ in self.requests]


@pytest.fixture
def config():
    return JiraConfig.from_env(ENV)


def push(transcript, items, out_dir, config, opener):
    extraction = make_extraction(items=items)
    return push_to_jira(route(extraction), verify(extraction, transcript), out_dir, config, opener=opener)


def test_bug_becomes_jira_issue_with_auth_and_payload(tmp_path, transcript, config):
    fake = FakeJira()
    item = make_item(due_date=date(2026, 10, 15), due_text="do czwartku", constraints=["tylko raz"])
    result = push(transcript, [item], tmp_path, config, fake)

    assert result.created == {"A01": "RIN-1"}
    request, timeout = fake.requests[0]
    assert request.full_url == "https://example.atlassian.net/rest/api/2/issue"
    assert request.get_method() == "POST"
    assert timeout == 30
    expected_auth = "Basic " + base64.b64encode(f"bot@example.com:{TOKEN}".encode()).decode()
    assert request.get_header("Authorization") == expected_auth
    assert request.get_header("Content-type") == "application/json"

    fields = fake.payloads()[0]["fields"]
    assert fields["project"] == {"key": "RIN"}
    assert fields["issuetype"] == {"name": "Bug"}
    assert fields["summary"] == "[Klient] Naprawić filtr"
    assert fields["labels"] == ["callflow"]
    assert fields["duedate"] == "2026-10-15"
    description = fields["description"]
    assert "Właściciel: Marek" in description
    assert "Termin: 2026-10-15 („do czwartku”)" in description
    assert "Ograniczenia: tylko raz" in description
    assert 'Anna (l. 7): „Filtr "zainteresowany" nie zawęża listy.”' in description
    assert description.endswith("Utworzone automatycznie przez callflow z rozmowy z 2026-10-13")


def test_config_change_uses_config_issue_type_and_other_inboxes_are_not_sent(tmp_path, transcript):
    config = JiraConfig.from_env(ENV | {"JIRA_ISSUE_TYPE_CONFIG": "Zmiana"})
    fake = FakeJira()
    items = [
        make_item(id="A01", kind=Kind.config_change),
        make_item(id="A02", kind=Kind.task),
        make_item(id="A03", kind=Kind.feature_request),
        make_item(id="A04", kind=Kind.bug, state=State.on_hold),
    ]
    result = push(transcript, items, tmp_path, config, fake)

    assert result.created == {"A01": "RIN-1"}
    fields = fake.payloads()[0]["fields"]
    assert fields["issuetype"] == {"name": "Zmiana"}
    assert "duedate" not in fields


def test_long_title_is_truncated_to_jira_summary_limit(tmp_path, transcript, config):
    fake = FakeJira()
    push(transcript, [make_item(title="x" * 400)], tmp_path, config, fake)
    assert len(fake.payloads()[0]["fields"]["summary"]) == 255


def test_unverified_item_is_skipped_for_human_review(tmp_path, transcript, config):
    fake = FakeJira()
    unverified = make_item(id="A02", evidence=[Evidence(speaker="Anna", quote="zmyślone zdanie")])
    result = push(transcript, [make_item(), unverified], tmp_path, config, fake)

    assert result.created == {"A01": "RIN-1"}
    assert [item_id for item_id, _ in result.skipped] == ["A02"]
    assert "human review" in result.skipped[0][1]
    assert len(fake.requests) == 1


def test_second_run_creates_nothing_thanks_to_mapping_file(tmp_path, transcript, config):
    items = [make_item(), make_item(id="A02", kind=Kind.config_change)]
    push(transcript, items, tmp_path, config, FakeJira())
    assert json.loads((tmp_path / JIRA_FILE).read_text(encoding="utf-8")) == {
        "A01 · Naprawić filtr": "RIN-1",
        "A02 · Naprawić filtr": "RIN-2",
    }

    fake = FakeJira()
    result = push(transcript, items, tmp_path, config, fake)
    assert fake.requests == []
    assert result.created == {}
    assert result.skipped == [("A01", "already in Jira as RIN-1"), ("A02", "already in Jira as RIN-2")]


def test_renumbered_item_from_a_new_run_is_not_mistaken_for_a_sent_one(tmp_path, transcript, config):
    push(transcript, [make_item()], tmp_path, config, FakeJira())

    fake = FakeJira()
    result = push(transcript, [make_item(title="Zmienić godziny dzwonienia")], tmp_path, config, fake)
    assert result.created == {"A01": "RIN-1"}
    assert len(fake.requests) == 1


def test_progress_is_kept_when_a_later_issue_fails(tmp_path, transcript, config):
    class FailSecond(FakeJira):
        def __call__(self, request, timeout):
            if self.requests:
                raise urllib.error.URLError("connection reset")
            return super().__call__(request, timeout)

    items = [make_item(), make_item(id="A02")]
    with pytest.raises(JiraError, match="cannot reach Jira"):
        push(transcript, items, tmp_path, config, FailSecond())
    assert json.loads((tmp_path / JIRA_FILE).read_text(encoding="utf-8")) == {"A01 · Naprawić filtr": "RIN-1"}


def test_http_error_carries_jira_message_but_never_the_token(tmp_path, transcript, config):
    body = json.dumps({"errorMessages": [f"bad token {TOKEN}"], "errors": {"issuetype": "invalid type"}})
    url = "https://example.atlassian.net/rest/api/2/issue"
    error = urllib.error.HTTPError(url, 400, "Bad Request", Message(), io.BytesIO(body.encode()))
    with pytest.raises(JiraError) as caught:
        push(transcript, [make_item()], tmp_path, config, FakeJira(fail_with=error))

    message = str(caught.value)
    assert "HTTP 400" in message
    assert "issuetype: invalid type" in message
    assert TOKEN not in message
    assert not (tmp_path / JIRA_FILE).exists()


def test_missing_settings_are_listed_by_name_only():
    with pytest.raises(JiraError) as caught:
        JiraConfig.from_env({"JIRA_BASE_URL": "https://x.atlassian.net", "JIRA_API_TOKEN": TOKEN})
    message = str(caught.value)
    assert "JIRA_EMAIL" in message and "JIRA_PROJECT_KEY" in message
    assert "JIRA_BASE_URL" not in message
    assert TOKEN not in message


def test_plain_http_base_url_is_rejected():
    with pytest.raises(JiraError, match="https"):
        JiraConfig.from_env(ENV | {"JIRA_BASE_URL": "http://example.atlassian.net"})


def test_token_is_not_in_config_repr(config):
    assert TOKEN not in repr(config)


def test_load_dotenv_parses_and_does_not_override(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "# Jira\n\nJIRA_EMAIL='bot@example.com'\nexport JIRA_PROJECT_KEY=\"RIN\"\n"
        "JIRA_API_TOKEN=abc=def\nJIRA_BASE_URL=https://from-file\nnot a setting\n",
        encoding="utf-8",
    )
    environ = {"JIRA_BASE_URL": "https://already-set"}
    load_dotenv(env_file, environ)

    assert environ == {
        "JIRA_BASE_URL": "https://already-set",
        "JIRA_EMAIL": "bot@example.com",
        "JIRA_PROJECT_KEY": "RIN",
        "JIRA_API_TOKEN": "abc=def",
    }


def test_load_dotenv_without_file_does_nothing(tmp_path):
    environ = {}
    load_dotenv(tmp_path / ".env", environ)
    assert environ == {}
