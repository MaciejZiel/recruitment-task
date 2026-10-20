import shutil
from pathlib import Path

from conftest import EXTRACTION_FIXTURE

from callflow import cli
from callflow.jira import JiraCheck, JiraPushResult

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPT = ROOT / "examples" / "transkrypcja-spotkanie.md"
JIRA_ENV = {
    "JIRA_BASE_URL": "https://example.atlassian.net",
    "JIRA_EMAIL": "a@example.com",
    "JIRA_API_TOKEN": "secret",
    "JIRA_PROJECT_KEY": "RIN",
}


def test_from_json_runs_offline(tmp_path, capsys):
    assert cli.main([str(TRANSCRIPT), "--out", str(tmp_path), "--from-json", str(EXTRACTION_FIXTURE)]) == 0
    assert "0 with unverified evidence" in capsys.readouterr().out
    for name in ("report.md", "report.html", "outbox.json"):
        assert (tmp_path / name).is_file()
    assert (tmp_path / "report.html").read_text(encoding="utf-8").startswith("<!doctype html>")


def test_missing_transcript_reports_error(tmp_path, capsys):
    assert cli.main([str(tmp_path / "nope.md"), "--out", str(tmp_path / "out")]) == 1
    assert "error:" in capsys.readouterr().err
    assert not (tmp_path / "out").exists()


def test_transcript_without_turns_is_rejected(tmp_path, capsys):
    empty = tmp_path / "empty.md"
    empty.write_text("# Notatka\n\nBez dialogu.\n", encoding="utf-8")
    assert cli.main([str(empty), "--out", str(tmp_path / "out")]) == 1
    assert "no speaker turns" in capsys.readouterr().err


def test_live_run_writes_raw_response_and_extraction(tmp_path, monkeypatch):
    def fake_extract(text, meeting_date, vendor, **kwargs):
        extraction = cli.load_extraction(EXTRACTION_FIXTURE)
        return extraction, {"total_cost_usd": None, "structured_output": {}}

    monkeypatch.setattr(cli, "extract", fake_extract)
    transcript = tmp_path / "call.md"
    shutil.copy(TRANSCRIPT, transcript)

    assert cli.main([str(transcript), "--out", str(tmp_path / "out")]) == 0
    assert (tmp_path / "out" / cli.EXTRACTION_FILE).is_file()
    assert (tmp_path / "out" / cli.RAW_RESPONSE_FILE).is_file()


def test_missing_meeting_date_warns_and_still_runs(tmp_path, monkeypatch, capsys):
    calls = []

    def fake_extract(text, meeting_date, vendor, **kwargs):
        calls.append(meeting_date)
        extraction = cli.load_extraction(EXTRACTION_FIXTURE).model_copy(
            update={"meeting_date": None, "items": []}
        )
        return extraction, {"total_cost_usd": 0.0}

    monkeypatch.setattr(cli, "extract", fake_extract)
    transcript = tmp_path / "call.md"
    transcript.write_text("Kasia: Filtr nie działa.\nMarek: Sprawdzę.\n", encoding="utf-8")

    assert cli.main([str(transcript), "--out", str(tmp_path / "out")]) == 0
    assert calls == [None]
    assert "meeting date not found" in capsys.readouterr().err
    assert "Data spotkania nieznana" in (tmp_path / "out" / "report.md").read_text(encoding="utf-8")


def set_jira_env(tmp_path, monkeypatch, env):
    monkeypatch.setattr(cli, "DOTENV_FILE", tmp_path / "missing.env")
    for name in (*JIRA_ENV, "JIRA_ISSUE_TYPE_BUG", "JIRA_ISSUE_TYPE_CONFIG"):
        monkeypatch.delenv(name, raising=False)
    for name, value in env.items():
        monkeypatch.setenv(name, value)


def jira_args(tmp_path, *flags):
    return [str(TRANSCRIPT), "--out", str(tmp_path / "out"), "--from-json", str(EXTRACTION_FIXTURE), *flags]


def test_jira_flag_pushes_after_writing_the_report(tmp_path, monkeypatch, capsys):
    pushed = []

    def fake_push(routed, report, out_dir, config):
        assert (out_dir / "report.md").is_file()
        assert (out_dir / "report.html").is_file()
        pushed.append(config.project_key)
        return JiraPushResult(created={"A08": "RIN-7"}, skipped=[("A03", "already in Jira as RIN-1")])

    monkeypatch.setattr(cli, "push_to_jira", fake_push)
    set_jira_env(tmp_path, monkeypatch, JIRA_ENV)

    assert cli.main(jira_args(tmp_path, "--jira")) == 0
    assert pushed == ["RIN"]
    out = capsys.readouterr().out
    assert "Jira: created RIN-7 for A08 (https://example.atlassian.net/browse/RIN-7)" in out
    assert "Jira: skipped A03" in out
    assert "Jira: 1 created, 1 skipped" in out


def test_jira_flag_without_settings_fails_before_any_work(tmp_path, monkeypatch, capsys):
    set_jira_env(tmp_path, monkeypatch, {})

    assert cli.main(jira_args(tmp_path, "--jira")) == 1
    assert "missing Jira settings: JIRA_BASE_URL" in capsys.readouterr().err
    assert not (tmp_path / "out").exists()


def test_jira_check_prints_findings_and_stops_on_problems(tmp_path, monkeypatch, capsys):
    def fake_check(config):
        return JiraCheck(
            user="Maciej",
            project="RIN (Rinvo)",
            issue_types=["Task", "Epic"],
            problems=["JIRA_ISSUE_TYPE_BUG='Bug' is not an issue type of RIN"],
        )

    monkeypatch.setattr(cli, "check_connection", fake_check)
    set_jira_env(tmp_path, monkeypatch, JIRA_ENV)

    assert cli.main(jira_args(tmp_path, "--jira-check", "--jira")) == 1
    captured = capsys.readouterr()
    assert "authenticated as Maciej" in captured.out
    assert "issue types: Task, Epic" in captured.out
    assert "issue type for bugs: Bug MISSING" in captured.out
    assert "issue type for config changes: Task OK" in captured.out
    assert "not an issue type" in captured.err
    assert not (tmp_path / "out").exists()


def test_jira_check_that_passes_continues_the_run(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "check_connection", lambda config: JiraCheck("M", "RIN (R)", ["Bug", "Task"]))
    set_jira_env(tmp_path, monkeypatch, JIRA_ENV)

    assert cli.main(jira_args(tmp_path, "--jira-check")) == 0
    assert (tmp_path / "out" / "report.md").is_file()
