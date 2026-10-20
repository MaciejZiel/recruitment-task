import json
from datetime import date

import pytest
from conftest import EXTRACTION_FIXTURE

from callflow import extract as extract_module
from callflow.llm import LLMResponse


def fake_llm(data, expected_date_line="MEETING_DATE: 2026-10-06"):
    def complete_json(system, user, schema, **kwargs):
        assert expected_date_line in user
        assert schema["title"] == "MeetingExtraction"
        return LLMResponse(data=data, raw={"structured_output": data})

    return complete_json


def test_valid_model_output_is_parsed(monkeypatch):
    data = json.loads(EXTRACTION_FIXTURE.read_text(encoding="utf-8"))
    monkeypatch.setattr(extract_module.llm, "complete_json", fake_llm(data))

    extraction, raw = extract_module.extract("**A:** x", date(2026, 10, 6), "Rinvo")

    assert extraction.meeting_date == date(2026, 10, 6)
    assert extraction.assumptions == data["assumptions"]
    assert raw == {"structured_output": data}


def test_schema_mismatch_keeps_raw_response(monkeypatch):
    monkeypatch.setattr(extract_module.llm, "complete_json", fake_llm({"items": "nope"}))

    with pytest.raises(extract_module.ExtractionError) as error:
        extract_module.extract("**A:** x", date(2026, 10, 6), "Rinvo")
    assert error.value.raw == {"structured_output": {"items": "nope"}}


def test_wrong_meeting_date_is_replaced_and_noted(monkeypatch):
    data = json.loads(EXTRACTION_FIXTURE.read_text(encoding="utf-8")) | {"meeting_date": "2026-10-20"}
    monkeypatch.setattr(extract_module.llm, "complete_json", fake_llm(data))

    extraction, _ = extract_module.extract("**A:** x", date(2026, 10, 6), "Rinvo")

    assert extraction.meeting_date == date(2026, 10, 6)
    assert extraction.assumptions[: len(data["assumptions"])] == data["assumptions"]
    assert extraction.assumptions[-1] == (
        "Model zwrócił datę spotkania 2026-10-20; użyto daty 2026-10-06 z transkrypcji lub parametru."
    )


def test_invented_date_for_unknown_meeting_is_dropped_and_noted(monkeypatch):
    data = json.loads(EXTRACTION_FIXTURE.read_text(encoding="utf-8")) | {"meeting_date": "2026-10-20"}
    monkeypatch.setattr(extract_module.llm, "complete_json", fake_llm(data, "MEETING_DATE: unknown"))

    extraction, _ = extract_module.extract("**A:** x", None, "Rinvo")

    assert extraction.meeting_date is None
    assert extraction.assumptions[-1] == (
        "Model zwrócił datę spotkania 2026-10-20; data spotkania pozostaje nieznana."
    )
