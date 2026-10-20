from datetime import date
from pathlib import Path

import pytest

from callflow.schema import ActionItem, Draft, Evidence, Guardrail, Kind, MeetingExtraction, State
from callflow.transcript import parse_transcript

EXTRACTION_FIXTURE = Path(__file__).parent / "fixtures" / "extraction.json"

TRANSCRIPT = """# Klient × Rinvo

13 października 2026 (wtorek).

## Transkrypcja

**Anna:** Filtr „zainteresowany” nie zawęża listy.
**Marek:** Sprawdzę to po callu.
**Anna:** I nie piszcie do Oli, wszystko ustalacie ze mną.
"""


def make_item(**overrides) -> ActionItem:
    fields = {
        "id": "A01",
        "title": "Naprawić filtr",
        "details": "Filtr statusu nie zawęża listy.",
        "kind": Kind.bug,
        "state": State.do_now,
        "owner": "Marek",
        "due_date": None,
        "due_text": None,
        "condition": None,
        "constraints": [],
        "approval_by": None,
        "final_value": None,
        "superseded": [],
        "depends_on": [],
        "evidence": [Evidence(speaker="Anna", quote='Filtr "zainteresowany" nie zawęża listy.')],
    }
    fields.update(overrides)
    return ActionItem(**fields)


def make_extraction(items=None, guardrails=None, drafts=None) -> MeetingExtraction:
    return MeetingExtraction(
        meeting_date=date(2026, 10, 13),
        client="Klient",
        participants=["Anna", "Marek"],
        summary="Krótko.",
        items=items if items is not None else [make_item()],
        guardrails=guardrails or [],
        drafts=drafts or [],
        assumptions=[],
    )


@pytest.fixture
def transcript():
    return parse_transcript(TRANSCRIPT)


@pytest.fixture
def guardrail():
    return Guardrail(
        rule="Nie pisać do Oli",
        until=None,
        approval_by=None,
        evidence=[Evidence(speaker="Anna", quote="nie piszcie do Oli")],
    )


@pytest.fixture
def draft():
    return Draft(
        to="Anna", subject="Filtr", body="Poprawione.", send_when="po naprawie", related_items=["A01"]
    )
