import shutil
from pathlib import Path

from callflow import cli
from callflow.jira import JiraPushResult

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPT = ROOT / "examples" / "transkrypcja-spotkanie.md"
FIXTURE = Path(__file__).parent / "fixtures" / "extraction.json"


def test_from_json_runs_offline(tmp_path, capsys):
    assert cli.main([str(TRANSCRIPT), "--out", str(tmp_path), "--from-json", str(FIXTURE)]) == 0
    assert "0 with unverified evidence" in capsys.readouterr().out


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
        extraction = cli.load_extraction(FIXTURE)
        return extraction, {"total_cost_usd": 0.0, "structured_output": {}}

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
        extraction = cli.load_extraction(FIXTURE).model_copy(update={"meeting_date": None, "items": []})
        return extraction, {"total_cost_usd": 0.0}

    monkeypatch.setattr(cli, "extract", fake_extract)
    transcript = tmp_path / "call.md"
    transcript.write_text("Kasia: Filtr nie działa.\nMarek: Sprawdzę.\n", encoding="utf-8")

    assert cli.main([str(transcript), "--out", str(tmp_path / "out")]) == 0
    assert calls == [None]
    assert "meeting date not found" in capsys.readouterr().err
    assert "Data spotkania nieznana" in (tmp_path / "out" / "report.md").read_text(encoding="utf-8")


def test_jira_flag_pushes_after_writing_the_report(tmp_path, monkeypatch, capsys):
    pushed = []

    def fake_push(routed, report, out_dir, config):
        assert (out_dir / "report.md").is_file()
        pushed.append(config.project_key)
        return JiraPushResult(created={"A08": "RIN-7"}, skipped=[("A03", "already in Jira as RIN-1")])

    monkeypatch.setattr(cli, "push_to_jira", fake_push)
    monkeypatch.setattr(cli, "DOTENV_FILE", tmp_path / "missing.env")
    for name, value in {
        "JIRA_BASE_URL": "https://example.atlassian.net",
        "JIRA_EMAIL": "a@example.com",
        "JIRA_API_TOKEN": "secret",
        "JIRA_PROJECT_KEY": "RIN",
    }.items():
        monkeypatch.setenv(name, value)

    args = [str(TRANSCRIPT), "--out", str(tmp_path / "out"), "--from-json", str(FIXTURE), "--jira"]
    assert cli.main(args) == 0
    assert pushed == ["RIN"]
    out = capsys.readouterr().out
    assert "Jira: created RIN-7 for A08" in out
    assert "Jira: skipped A03" in out


def test_jira_flag_without_settings_fails_clearly(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli, "DOTENV_FILE", tmp_path / "missing.env")
    for name in ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT_KEY"):
        monkeypatch.delenv(name, raising=False)

    args = [str(TRANSCRIPT), "--out", str(tmp_path / "out"), "--from-json", str(FIXTURE), "--jira"]
    assert cli.main(args) == 1
    assert "missing Jira settings: JIRA_BASE_URL" in capsys.readouterr().err
