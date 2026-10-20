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
    assert (len(main.turns), len(second.turns)) == (108, 22)


def test_year_followed_by_r_suffix_is_parsed():
    assert parse_call_date("Spotkanie 14.10.2026r., Teams") == date(2026, 10, 14)
    assert parse_call_date("6 października 2026r.") == date(2026, 10, 6)
    assert parse_call_date("2026-10-13r.") == date(2026, 10, 13)
    assert parse_call_date("14.10.20261") is None


def test_bold_label_with_timestamp_inside():
    transcript = parse_transcript("**[00:01] Kasia:** Cześć.\n**[00:02:15] Marek**: Hej.\n")
    assert [(t.speaker, t.text) for t in transcript.turns] == [("Kasia", "Cześć."), ("Marek", "Hej.")]


def test_parses_dotted_date_and_rejects_impossible_dates():
    assert parse_call_date("Spotkanie 06.10.2026, Teams") == date(2026, 10, 6)
    assert parse_call_date("32.13.2026") is None


def test_plain_speaker_labels_are_used_when_no_bold_turns():
    text = "Rozmowa 06.10.2026\n\n[00:00:05] Kasia: Filtr nie działa.\nMarek: Sprawdzę to.\n"
    transcript = parse_transcript(text)

    assert transcript.call_date == "2026-10-06"
    assert [(t.line, t.speaker, t.text) for t in transcript.turns] == [
        (3, "Kasia", "Filtr nie działa."),
        (4, "Marek", "Sprawdzę to."),
    ]


def test_bold_turns_take_precedence_over_plain_labels():
    transcript = parse_transcript("**Kasia:** Cześć.\nUwaga: to nie jest wypowiedź.\n")
    assert [t.speaker for t in transcript.turns] == ["Kasia"]


def test_colon_outside_bold_label_is_a_turn():
    transcript = parse_transcript("**Kasia**: Filtr nie działa.\n**Marek**: Sprawdzę.\n")
    assert [(t.speaker, t.text) for t in transcript.turns] == [
        ("Kasia", "Filtr nie działa."),
        ("Marek", "Sprawdzę."),
    ]


def test_utterance_spanning_lines_and_paragraphs_is_joined():
    text = (
        "## Transkrypcja\n\n**Kasia:** Pierwszy akapit.\n\nDrugi akapit z ustaleniem.\n**Marek:** Dobrze.\n"
    )
    transcript = parse_transcript(text)
    assert [(t.line, t.text) for t in transcript.turns] == [
        (3, "Pierwszy akapit. Drugi akapit z ustaleniem."),
        (6, "Dobrze."),
    ]


def test_plain_utterance_continuation_is_joined():
    transcript = parse_transcript("Kasia: Pierwsza linia\ndruga linia.\nMarek: Ok.\n")
    assert [t.text for t in transcript.turns] == ["Pierwsza linia druga linia.", "Ok."]


def test_utf8_bom_from_notepad_is_ignored(tmp_path):
    path = tmp_path / "call.md"
    path.write_text("**Kasia:** Cześć.\n**Marek:** Hej.\n", encoding="utf-8-sig")
    assert [t.speaker for t in load_transcript(path).turns] == ["Kasia", "Marek"]


def test_earliest_valid_date_in_line_wins():
    assert parse_call_date("6 października 2026 (wtorek), notatka z 2026-09-01") == date(2026, 10, 6)
    assert parse_call_date("2026-13-45, potem 06.10.2026") == date(2026, 10, 6)


def test_date_mentioned_in_an_utterance_is_not_the_meeting_date():
    transcript = parse_transcript("Kasia: Proszę o raport do 15 listopada 2026.\nMarek: Dobrze.\n")
    assert transcript.call_date is None


def test_colon_sentence_inside_plain_utterance_is_not_a_speaker():
    text = (
        "Agnieszka: Zgłosiłam to w piątek.\n"
        "I mówię od razu: chcę, żeby to było naprawione.\n"
        "Tu mam napisane: do końca miesiąca.\n"
        "[00:12:05] Speaker 1: Rozumiem.\n"
        "Kasia Malinowska: Ok.\n"
    )
    transcript = parse_transcript(text)
    assert [(t.line, t.speaker) for t in transcript.turns] == [
        (1, "Agnieszka"),
        (4, "Speaker 1"),
        (5, "Kasia Malinowska"),
    ]
    assert transcript.turns[0].text == (
        "Zgłosiłam to w piątek. I mówię od razu: chcę, żeby to było naprawione."
        " Tu mam napisane: do końca miesiąca."
    )


def test_header_labels_before_first_plain_turn_are_metadata():
    transcript = parse_transcript("Temat: wdrożenie\nData: 2026-10-06\nKasia: Cześć.\nMarek: Hej.\n")
    assert transcript.call_date == "2026-10-06"
    assert transcript.header_lines == ["Temat: wdrożenie", "Data: 2026-10-06"]
    assert [t.speaker for t in transcript.turns] == ["Kasia", "Marek"]


def test_every_example_transcript_yields_only_real_speakers():
    expected = {
        "transkrypcja-spotkanie.md": ({"Kasia", "Marek"}, 108),
        "druga-rozmowa.md": ({"Agnieszka", "Marek"}, 22),
        "synthetic/fitstudio-rozmowa.md": ({"Agnieszka", "Marek"}, None),
    }
    for name, (speakers, count) in expected.items():
        transcript = load_transcript(EXAMPLES / name)
        assert {t.speaker for t in transcript.turns} == speakers, name
        if count is not None:
            assert len(transcript.turns) == count, name


def test_plain_label_with_parenthetical_role():
    transcript = parse_transcript("Marek (Rinvo): Cześć.\nMarek Rewoliński (Rinvo): Hej.\nKasia: Ok.\n")
    assert [t.speaker for t in transcript.turns] == ["Marek (Rinvo)", "Marek Rewoliński (Rinvo)", "Kasia"]


def test_plain_label_with_meet_timestamp_suffix():
    transcript = parse_transcript(
        "Kasia Malinowska (11:02): Dzień dobry.\nMarek (00:01:15): Cześć.\nKasia Malinowska (11:03): Ok.\n"
    )
    assert [t.speaker for t in transcript.turns] == ["Kasia Malinowska", "Marek", "Kasia Malinowska"]
    assert [t.text for t in transcript.turns] == ["Dzień dobry.", "Cześć.", "Ok."]
