from datetime import date

from conftest import make_extraction, make_item

from callflow.schema import Draft, Evidence, State
from callflow.verify import normalize, same_speaker_label, verify


def messages(report):
    return [(issue.owner_id, issue.message) for issue in report.issues]


def test_normalize_unifies_quotes_dashes_and_whitespace():
    assert normalize("„Ala”  ma –\n kota") == normalize('"ala" ma - kota')


def test_verbatim_quote_is_verified_with_line(transcript, guardrail, draft):
    report = verify(make_extraction(guardrails=[guardrail], drafts=[draft]), transcript)

    assert report.issues == []
    assert [check.line for check in report.quotes] == [7, 9]
    assert report.unverified_ids() == set()


def test_invented_quote_is_flagged(transcript):
    item = make_item(evidence=[Evidence(speaker="Anna", quote="Wyłączcie wszystko od jutra.")])
    report = verify(make_extraction(items=[item]), transcript)

    assert report.unverified_ids() == {"A01"}
    assert "nie występuje w transkrypcji" in messages(report)[0][1]


def test_quote_attributed_to_wrong_speaker_is_flagged(transcript):
    item = make_item(evidence=[Evidence(speaker="Marek", quote="nie zawęża listy")])
    report = verify(make_extraction(items=[item]), transcript)

    assert report.unverified_ids() == {"A01"}
    assert messages(report) == [("A01", "cytat z linii 7 nie pochodzi od 'Marek'")]


def test_field_consistency_checks(transcript):
    items = [
        make_item(id="A01", due_date=date(2026, 10, 1)),
        make_item(id="A02", owner=None),
        make_item(id="A03", state=State.scheduled, depends_on=["A99"]),
        make_item(id="A03"),
        make_item(id="A04", evidence=[]),
    ]
    found = messages(verify(make_extraction(items=items), transcript))

    assert ("A03", "id występuje 2 razy") in found
    assert ("A01", "termin 2026-10-01 jest przed datą spotkania") in found
    assert ("A02", "pozycja do wykonania bez właściciela") in found
    assert ("A03", "stan 'scheduled' bez terminu") in found
    assert ("A03", "zależność od nieistniejącej pozycji A99") in found
    assert ("A04", "brak cytatu-dowodu") in found


def test_draft_links_are_checked(transcript):
    drafts = [
        Draft(to="Anna", subject="x", body="y", send_when="z", related_items=[]),
        Draft(to="Anna", subject="x", body="y", send_when="z", related_items=["A42"]),
    ]
    found = messages(verify(make_extraction(drafts=drafts), transcript))

    assert ("D01", "szkic nie jest powiązany z żadną pozycją") in found
    assert ("D02", "powiązanie z nieistniejącą pozycją A42") in found


def test_full_name_from_model_matches_first_name_label(transcript):
    item = make_item(evidence=[Evidence(speaker="Anna Nowak", quote="nie zawęża listy")])
    report = verify(make_extraction(items=[item]), transcript)
    assert report.issues == []


def test_different_speaker_with_shared_prefix_does_not_match():
    assert not same_speaker_label("Ania", "Anna")
    assert same_speaker_label("Marek", "Marek Rewoliński")
