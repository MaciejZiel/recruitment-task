import shutil
from pathlib import Path

from conftest import EXTRACTION_FIXTURE

from callflow import cli

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPT = ROOT / "examples" / "transkrypcja-spotkanie.md"


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
