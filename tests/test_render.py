import json

from conftest import make_extraction, make_item

from callflow.render import OUTBOX_FILE, REPORT_FILE, draft_paths, render_report, write_outputs
from callflow.route import Inbox, route
from callflow.schema import Draft, Evidence, Kind, State
from callflow.verify import verify


def report_text(extraction, transcript):
    return render_report(route(extraction), verify(extraction, transcript), "call.md")


def test_html_from_model_or_transcript_is_neutralised(transcript):
    item = make_item(title="<script>alert(1)</script>", details="a & b")
    extraction = make_extraction(items=[item])
    text = report_text(extraction, transcript)

    assert "<script>" not in text
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in text
    assert "a &amp; b" in text


def test_guardrails_come_before_work_sections_and_quotes_show_lines(transcript, guardrail):
    extraction = make_extraction(guardrails=[guardrail])
    text = report_text(extraction, transcript)

    assert text.index("## Zabezpieczenia") < text.index(f"## {Inbox.tickets.value}")
    assert "Anna (l. 9) ✅" in text


def test_unverified_item_is_flagged(transcript):
    item = make_item(evidence=[Evidence(speaker="Anna", quote="zmyślone zdanie")])
    extraction = make_extraction(items=[item])
    text = report_text(extraction, transcript)

    assert "A01 · Naprawić filtr ⚠️ do sprawdzenia" in text
    assert "brak w transkrypcji" in text


def test_call_without_agreements_says_so(transcript):
    extraction = make_extraction(items=[])
    text = report_text(extraction, transcript)
    assert "Brak ustaleń wymagających działania" in text


def test_write_outputs_creates_report_outbox_and_drafts(tmp_path, transcript, draft):
    items = [make_item(), make_item(id="A02", kind=Kind.feature_request, state=State.do_not_do)]
    extraction = make_extraction(items=items, drafts=[draft])
    write_outputs(route(extraction), verify(extraction, transcript), tmp_path, "call.md")

    outbox = json.loads((tmp_path / OUTBOX_FILE).read_text(encoding="utf-8"))
    assert outbox["requires_approval"] is True
    assert [item["id"] for item in outbox["inboxes"]["tickets"]["items"]] == ["A01"]
    assert [item["id"] for item in outbox["inboxes"]["do_not_do"]["items"]] == ["A02"]
    assert (tmp_path / REPORT_FILE).is_file()
    assert (tmp_path / "drafts" / "D01-anna.md").read_text(encoding="utf-8").startswith("**Do:** Anna")


def test_draft_file_names_are_readable():
    drafts = [
        Draft(
            to="Kasia Malinowska <kasia@x.pl>", subject="s", body="b", send_when="w", related_items=["A01"]
        ),
        Draft(to="Paweł (Grupa Auto Tama)", subject="s", body="b", send_when="w", related_items=["A01"]),
    ]
    assert draft_paths(drafts) == ["drafts/D01-kasia-malinowska.md", "drafts/D02-pawel.md"]
