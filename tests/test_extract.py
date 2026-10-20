import json
from datetime import date

import pytest
from conftest import EXTRACTION_FIXTURE

from callflow import extract as extract_module
from callflow.llm import LLMResponse


def fake_llm(data):
    def complete_json(system, user, schema, **kwargs):
        assert "MEETING_DATE: 2026-10-06" in user
        assert schema["title"] == "MeetingExtraction"
        return LLMResponse(data=data, raw={"structured_output": data})

    return complete_json


def test_valid_model_output_is_parsed(monkeypatch):
    data = json.loads(EXTRACTION_FIXTURE.read_text(encoding="utf-8"))
    monkeypatch.setattr(extract_module.llm, "complete_json", fake_llm(data))

    extraction, raw = extract_module.extract("**A:** x", date(2026, 10, 6), "Rinvo")

    assert extraction.meeting_date == date(2026, 10, 6)
    assert raw == {"structured_output": data}


def test_schema_mismatch_keeps_raw_response(monkeypatch):
    monkeypatch.setattr(extract_module.llm, "complete_json", fake_llm({"items": "nope"}))

    with pytest.raises(extract_module.ExtractionError) as error:
        extract_module.extract("**A:** x", date(2026, 10, 6), "Rinvo")
    assert error.value.raw == {"structured_output": {"items": "nope"}}


def test_wrong_meeting_date_is_rejected(monkeypatch):
    data = json.loads(EXTRACTION_FIXTURE.read_text(encoding="utf-8")) | {"meeting_date": "2026-10-20"}
    monkeypatch.setattr(extract_module.llm, "complete_json", fake_llm(data))

    with pytest.raises(extract_module.ExtractionError, match="expected 2026-10-06"):
        extract_module.extract("**A:** x", date(2026, 10, 6), "Rinvo")
