"""Turn a parsed transcript into a validated MeetingExtraction using the model."""

from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import ValidationError

from callflow import llm
from callflow.prompt import SYSTEM_PROMPT, build_user_message
from callflow.schema import MeetingExtraction


class ExtractionError(RuntimeError):
    def __init__(self, message: str, raw: dict[str, Any] | None = None):
        super().__init__(message)
        self.raw = raw


def extract(
    transcript_text: str,
    meeting_date: date | None,
    vendor: str,
    *,
    model: str = llm.DEFAULT_MODEL,
    effort: str = llm.DEFAULT_EFFORT,
) -> tuple[MeetingExtraction, dict[str, Any]]:
    response = llm.complete_json(
        SYSTEM_PROMPT,
        build_user_message(transcript_text, meeting_date, vendor),
        MeetingExtraction.model_json_schema(),
        model=model,
        effort=effort,
    )
    try:
        extraction = MeetingExtraction.model_validate(response.data)
    except ValidationError as exc:
        raise ExtractionError(f"model output does not match the schema:\n{exc}", response.raw) from exc
    return _with_known_date(extraction, meeting_date), response.raw


def _with_known_date(extraction: MeetingExtraction, meeting_date: date | None) -> MeetingExtraction:
    """Keep the date the program knows; a differing model date is noted, not fatal after a paid run."""
    if extraction.meeting_date == meeting_date:
        return extraction
    returned = extraction.meeting_date or "brak"
    if meeting_date is None:
        kept = "data spotkania pozostaje nieznana"
    else:
        kept = f"użyto daty {meeting_date} z transkrypcji lub parametru"
    note = f"Model zwrócił datę spotkania {returned}; {kept}."
    return extraction.model_copy(
        update={"meeting_date": meeting_date, "assumptions": [*extraction.assumptions, note]}
    )
