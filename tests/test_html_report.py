import json
import re
from html.parser import HTMLParser
from pathlib import Path

from conftest import make_extraction, make_item

from callflow.html_report import EMPTY_CALL_NOTE, NO_CHANGES_NOTICE, render_html
from callflow.render import MISSING_DATE_NOTE, render_report
from callflow.route import Inbox, route
from callflow.schema import Draft, Evidence, MeetingExtraction, State
from callflow.transcript import load_transcript
from callflow.verify import verify

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = Path(__file__).parent / "fixtures" / "extraction.json"

VOID_TAGS = {"meta", "link", "br", "hr", "img", "input"}


def render(extraction, transcript, source_name="call.md") -> str:
    return render_html(route(extraction), verify(extraction, transcript), source_name)


class TagBalance(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"unexpected </{tag}> with open {self.stack[-3:]}")
        else:
            self.stack.pop()


def test_result_is_a_complete_well_formed_document(transcript, guardrail, draft):
    extraction = make_extraction(guardrails=[guardrail], drafts=[draft])
    page = render(extraction, transcript)

    assert page.startswith("<!doctype html>\n")
    assert '<html lang="pl">' in page
    assert '<meta charset="utf-8">' in page
    assert 'name="viewport"' in page
    assert "<title>Po rozmowie: Klient, 2026-10-13 · callflow</title>" in page
    assert page.rstrip().endswith("</html>")
    parser = TagBalance()
    parser.feed(page)
    assert parser.errors == []
    assert parser.stack == []


def test_model_and_transcript_text_is_escaped(transcript):
    payload = "<script>alert(1)</script>"
    item = make_item(title=payload, details="a & b", evidence=[Evidence(speaker="Anna", quote=payload)])
    bad_draft = Draft(
        to='Anna" onmouseover="x', subject=payload, body=payload, send_when="teraz", related_items=["A01"]
    )
    extraction = make_extraction(items=[item], drafts=[bad_draft])
    page = render(extraction, transcript, source_name='call"<b>.md')

    assert "alert(1)</script>" not in page
    assert page.count("<script>") == 1  # only the page's own filter script
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page
    assert "a &amp; b" in page
    assert "Anna&quot; onmouseover=&quot;x" in page
    assert "call&quot;&lt;b&gt;.md" in page


def test_sections_follow_report_md_order(transcript, guardrail, draft):
    extraction = make_extraction(guardrails=[guardrail], drafts=[draft]).model_copy(
        update={"assumptions": ["Założenie"]}
    )
    page = render(extraction, transcript)

    order = [
        NO_CHANGES_NOTICE,
        "<h2>Podsumowanie</h2>",
        "<h2>Zabezpieczenia",
        f"<h2>{Inbox.tickets.value}</h2>",
        "<h2>Szkice wiadomości",
        "<h2>Założenia",
    ]
    positions = [page.index(marker) for marker in order]
    assert positions == sorted(positions)


def test_headings_match_markdown_report_for_fixture():
    extraction = MeetingExtraction.model_validate(json.loads(FIXTURE.read_text(encoding="utf-8")))
    transcript = load_transcript(ROOT / "examples" / "transkrypcja-spotkanie.md")
    routed, report = route(extraction), verify(extraction, transcript)

    markdown = render_report(routed, report, "call.md")
    page = render_html(routed, report, "call.md")

    assert re.findall(r"<h2>(.*?)</h2>", page) == re.findall(r"^## (.*)$", markdown, re.MULTILINE)
    for item in extraction.items:
        assert f'id="{item.id}"' in page


def test_guardrail_shows_limits_and_verified_quote_line(transcript, guardrail):
    guardrail = guardrail.model_copy(update={"until": "do odwołania", "approval_by": "Anna"})
    page = render(make_extraction(guardrails=[guardrail]), transcript)

    assert '<span class="card-id">G01</span>Nie pisać do Oli' in page
    assert "<strong>do:</strong> do odwołania" in page
    assert "<strong>zdejmuje:</strong> Anna" in page
    assert "<strong>Anna</strong> (l. 9) ✅" in page


def test_unverified_item_is_flagged(transcript):
    item = make_item(evidence=[Evidence(speaker="Anna", quote="zmyślone zdanie")])
    page = render(make_extraction(items=[item]), transcript)

    assert '<span class="flag">⚠️ do sprawdzenia</span>' in page
    assert "needs-review" in page
    assert "(brak w transkrypcji) ⚠️ niezweryfikowany" in page
    assert '<li class="stat-warn">Cytaty zweryfikowane: <strong>0/1</strong></li>' in page


def test_verified_item_has_no_flag(transcript):
    page = render(make_extraction(), transcript)
    assert "do sprawdzenia" not in page


def test_do_not_do_state_is_marked_and_absent_facts_are_skipped(transcript):
    item = make_item(state=State.do_not_do, condition=None)
    page = render(make_extraction(items=[item]), transcript)

    assert 'class="card item do-not-do"' in page
    assert '<span class="badge state-do_not_do">do_not_do</span>' in page
    assert "<dt>Właściciel</dt><dd>Marek</dd>" in page
    assert "<dt>Warunek</dt>" not in page


def test_missing_meeting_date_is_announced(transcript):
    extraction = make_extraction().model_copy(update={"meeting_date": None})
    page = render(extraction, transcript)

    assert "Po rozmowie: Klient, data nieznana" in page
    assert MISSING_DATE_NOTE.removeprefix("> ") in page


def test_known_meeting_date_has_no_warning(transcript):
    page = render(make_extraction(), transcript)
    assert "Data spotkania nieznana" not in page


def test_call_without_agreements_says_so(transcript):
    page = render(make_extraction(items=[]), transcript)
    assert EMPTY_CALL_NOTE in page


def test_draft_keeps_line_breaks_and_links_its_file(transcript):
    draft = Draft(
        to="Anna",
        subject="Filtr",
        body="Cześć,\n\nfiltr działa.\n\nMarek",
        send_when="po naprawie",
        related_items=["A01"],
    )
    page = render(make_extraction(drafts=[draft]), transcript)

    assert '<div class="draft-body">Cześć,\n\nfiltr działa.\n\nMarek</div>' in page
    assert "white-space: pre-wrap" in page
    assert '<a href="drafts/D01-anna.md">drafts/D01-anna.md</a>' in page
    assert '<dt>Dotyczy</dt><dd><a href="#A01">A01</a></dd>' in page
