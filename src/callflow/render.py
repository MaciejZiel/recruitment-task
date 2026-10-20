"""Write the routed meeting as a human report, a machine-readable outbox and message drafts."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

from callflow.route import INBOX_ORDER, TARGET_SYSTEM, RoutedMeeting
from callflow.schema import ActionItem, Draft, Evidence
from callflow.verify import VerificationReport

REPORT_FILE = "report.md"
OUTBOX_FILE = "outbox.json"
DRAFTS_DIR = "drafts"
MISSING_DATE_NOTE = (
    "> ⚠️ Data spotkania nieznana: terminy względne (np. „do czwartku”) nie zostały przeliczone na daty."
)


def md(text: str) -> str:
    """Neutralise HTML in model/transcript text; GitHub would otherwise render raw tags."""
    return escape(text, quote=False)


def render_evidence(owner_id: str, evidence: list[Evidence], report: VerificationReport) -> list[str]:
    lines = []
    for check in report.quotes_for(owner_id):
        where = f"l. {check.line}" if check.line else "brak w transkrypcji"
        mark = "✅" if check.verified else "⚠️ niezweryfikowany"
        lines.append(f"  > {md(check.speaker)} ({where}) {mark}: „{md(check.quote)}”")
    if not evidence:
        lines.append("  > ⚠️ brak cytatu")
    return lines


def render_item(item: ActionItem, report: VerificationReport) -> list[str]:
    flag = " ⚠️ do sprawdzenia" if item.id in report.unverified_ids() else ""
    lines = [
        f"#### {item.id} · {md(item.title)}{flag}",
        f"`{item.kind}` · `{item.state}`  ",
        md(item.details),
    ]
    facts = [
        ("Właściciel", item.owner),
        ("Termin", _due(item)),
        ("Warunek", item.condition),
        ("Zatwierdza", item.approval_by),
        ("Wersja ostateczna", item.final_value),
        ("Zastępuje", "; ".join(item.superseded)),
        ("Ograniczenia", "; ".join(item.constraints)),
        ("Zależy od", ", ".join(item.depends_on)),
    ]
    lines += [f"- **{label}:** {md(value)}" for label, value in facts if value]
    lines += render_evidence(item.id, item.evidence, report)
    return lines + [""]


def _due(item: ActionItem) -> str | None:
    if item.due_date and item.due_text:
        return f"{item.due_date} („{item.due_text}”)"
    if item.due_date:
        return str(item.due_date)
    return f"bez daty („{item.due_text}”)" if item.due_text else None


def render_report(routed: RoutedMeeting, report: VerificationReport, source_name: str) -> str:
    extraction = routed.extraction
    verified = sum(check.verified for check in report.quotes)
    lines = [
        f"# Po rozmowie: {md(extraction.client)}, {extraction.meeting_date or 'data nieznana'}",
        "",
        f"Źródło: `{source_name}` · uczestnicy: {md(', '.join(extraction.participants))}  ",
        f"Pozycji: {len(extraction.items)} · zabezpieczeń: {len(extraction.guardrails)} · "
        f"szkiców: {len(extraction.drafts)} · cytaty zweryfikowane: {verified}/{len(report.quotes)}",
        "",
        "> Nic nie zostało wysłane ani zmienione. Każde działanie zewnętrzne czeka na zatwierdzenie.",
        "",
    ]
    if extraction.meeting_date is None:
        lines += [MISSING_DATE_NOTE, ""]
    lines += [
        "## Podsumowanie",
        "",
        md(extraction.summary),
        "",
    ]
    if not extraction.items and not extraction.guardrails:
        lines += ["**Brak ustaleń wymagających działania.**", ""]
    if extraction.guardrails:
        lines += ["## Zabezpieczenia (sprawdzić przed każdym działaniem)", ""]
    for index, guardrail in enumerate(extraction.guardrails, 1):
        guardrail_id = f"G{index:02d}"
        details = [
            f"do: {guardrail.until}" if guardrail.until else "",
            f"zdejmuje: {guardrail.approval_by}" if guardrail.approval_by else "",
        ]
        suffix = " · ".join(part for part in details if part)
        lines.append(f"- **{guardrail_id}** {md(guardrail.rule)}" + (f" ({md(suffix)})" if suffix else ""))
        lines += render_evidence(guardrail_id, guardrail.evidence, report)
    lines.append("")

    if report.issues:
        lines += ["## Ostrzeżenia walidacji", ""]
        lines += [f"- **{issue.owner_id}**: {md(issue.message)}" for issue in report.issues]
        lines.append("")

    if routed.calendar:
        lines += ["## Terminy (kalendarz i przypomnienia)", ""]
        for item in routed.calendar:
            limits = f" · {md('; '.join(item.constraints))}" if item.constraints else ""
            lines.append(f"- **{item.due_date}** · {item.id} {md(item.title)}{limits}")
        lines.append("")

    for inbox in INBOX_ORDER:
        items = routed.inboxes[inbox]
        if not items:
            continue
        lines += [f"## {inbox.value}", "", f"_Cel: {TARGET_SYSTEM[inbox]}_", ""]
        for item in items:
            lines += render_item(item, report)

    if extraction.drafts:
        lines += ["## Szkice wiadomości (do zatwierdzenia)", ""]
        for index, (draft, path) in enumerate(
            zip(extraction.drafts, draft_paths(extraction.drafts), strict=True), 1
        ):
            lines.append(
                f"- **D{index:02d}** do: {md(draft.to)} · „{md(draft.subject)}” · wysłać: "
                f"{md(draft.send_when)} · [{path}]({path})"
            )
        lines.append("")

    if extraction.assumptions:
        lines += ["## Założenia przyjęte przy analizie", ""]
        lines += [f"- {md(assumption)}" for assumption in extraction.assumptions]
        lines.append("")
    return "\n".join(lines)


def draft_paths(drafts: list[Draft]) -> list[str]:
    return [f"{DRAFTS_DIR}/D{index:02d}-{_slug(draft.to)}.md" for index, draft in enumerate(drafts, 1)]


_POLISH_TO_ASCII = str.maketrans("ąćęłńóśźż", "acelnoszz")


def _slug(recipient: str) -> str:
    name = re.split(r"[<(,]", recipient)[0].lower().translate(_POLISH_TO_ASCII)
    return re.sub(r"[^a-z0-9]+", "-", name).strip("-")[:30] or "draft"


def render_draft(draft: Draft) -> str:
    return (
        f"**Do:** {md(draft.to)}  \n**Temat:** {md(draft.subject)}  \n"
        f"**Wysłać:** {md(draft.send_when)}  \n**Dotyczy:** {', '.join(draft.related_items)}\n\n"
        f"---\n\n{md(draft.body)}\n"
    )


def build_outbox(routed: RoutedMeeting, report: VerificationReport) -> dict:
    unverified = report.unverified_ids()
    return {
        "meeting_date": routed.extraction.meeting_date and routed.extraction.meeting_date.isoformat(),
        "client": routed.extraction.client,
        "requires_approval": True,
        "inboxes": {
            inbox.name: {
                "target": TARGET_SYSTEM[inbox],
                "items": [
                    item.model_dump(mode="json") | {"needs_review": item.id in unverified}
                    for item in routed.inboxes[inbox]
                ],
            }
            for inbox in INBOX_ORDER
        },
        "calendar": [{"date": item.due_date.isoformat(), "item": item.id} for item in routed.calendar],
        "guardrails": [guardrail.model_dump(mode="json") for guardrail in routed.extraction.guardrails],
        "drafts": [draft.model_dump(mode="json") for draft in routed.extraction.drafts],
        "issues": [{"id": issue.owner_id, "message": issue.message} for issue in report.issues],
    }


def write_outputs(routed: RoutedMeeting, report: VerificationReport, out_dir: Path, source_name: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / REPORT_FILE).write_text(render_report(routed, report, source_name), encoding="utf-8")
    write_json(out_dir / OUTBOX_FILE, build_outbox(routed, report))

    drafts_dir = out_dir / DRAFTS_DIR
    drafts_dir.mkdir(exist_ok=True)
    for stale in drafts_dir.glob("D*.md"):
        stale.unlink()
    for draft, relative in zip(routed.extraction.drafts, draft_paths(routed.extraction.drafts), strict=True):
        (out_dir / relative).write_text(render_draft(draft), encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
