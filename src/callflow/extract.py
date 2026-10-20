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
    meeting_date: date,
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
    if extraction.meeting_date != meeting_date:
        raise ExtractionError(
            f"model returned meeting_date {extraction.meeting_date}, expected {meeting_date}", response.raw
        )
    return extraction, response.raw
