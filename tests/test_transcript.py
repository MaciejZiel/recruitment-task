from datetime import date
from pathlib import Path

from callflow.transcript import load_transcript, parse_call_date, parse_transcript

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"

SAMPLE = """# Klient × Rinvo

13 października 2026 (wtorek), Google Meet.

## Kontekst

**Słowniczek:** BDC – dział leadów.

## Uczestnicy

- **Anna Nowak**, klient, anna@example.com

## Transkrypcja

**Anna:** Filtr nie działa.

*[10:00–10:01] Anna wyciszona.*

**Marek:** Sprawdzę to dzisiaj.
"""


def test_parses_polish_date_from_header():
    assert parse_call_date("6 października 2026 (wtorek), 11:02") == date(2026, 10, 6)


def test_parses_iso_date():
    assert parse_call_date("Spotkanie 2026-10-13") == date(2026, 10, 13)


def test_missing_date_returns_none():
    assert parse_call_date("bez daty") is None
    assert parse_transcript("**A:** Cześć.").call_date is None


def test_turns_only_from_transcript_section():
    transcript = parse_transcript(SAMPLE)

    assert transcript.call_date == "2026-10-13"
    assert [(t.speaker, t.text) for t in transcript.turns] == [
        ("Anna", "Filtr nie działa."),
        ("Marek", "Sprawdzę to dzisiaj."),
    ]
    assert "**Słowniczek:** BDC – dział leadów." in transcript.sections["Kontekst"]
    assert [p.name for p in transcript.participants] == ["Anna Nowak"]
    assert transcript.stage_directions[0].text.startswith("[10:00–10:01]")


def test_turn_line_numbers_point_at_source():
    transcript = parse_transcript(SAMPLE)
    lines = SAMPLE.splitlines()
    for turn in transcript.turns:
        assert turn.text in lines[turn.line - 1]


def test_without_sections_every_bold_label_is_a_turn():
    transcript = parse_transcript("**A:** Cześć.\n**B:** Hej.\n")
    assert [t.speaker for t in transcript.turns] == ["A", "B"]


def test_example_transcripts_parse():
    main = load_transcript(EXAMPLES / "transkrypcja-spotkanie.md")
    assert main.call_date == "2026-10-06"
    assert {t.speaker for t in main.turns} == {"Kasia", "Marek"}

    second = load_transcript(EXAMPLES / "druga-rozmowa.md")
    assert second.call_date == "2026-10-13"
    assert second.turns
