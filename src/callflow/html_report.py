"""Render the routed meeting as a self-contained HTML page with the same content and order as report.md."""

from __future__ import annotations

import re
from html import escape

from callflow.render import MISSING_DATE_NOTE, _due, draft_paths
from callflow.route import INBOX_ORDER, TARGET_SYSTEM, Inbox, RoutedMeeting
from callflow.schema import ActionItem, Draft, Evidence, Guardrail, State
from callflow.verify import VerificationReport

NO_CHANGES_NOTICE = (
    "Nic nie zostało wysłane ani zmienione. Każde działanie zewnętrzne czeka na zatwierdzenie."
)
EMPTY_CALL_NOTE = "Brak ustaleń wymagających działania."

FONT_LINK = (
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@'
    '0,9..40,400..700;1,9..40,400..700&amp;display=swap">'
)

STYLE = """
/* Design tokens inspired by rinvo.io: navy surfaces, deep-blue primary, green accent, DM Sans. */
:root {
  --navy-950: #050e1a;
  --navy-900: #0a1628;
  --navy-700: #1a2d45;
  --surface: #ffffff;
  --surface-light: #f7fafd;
  --surface-mid: #eef3f8;
  --border: #e3e9f0;
  --text: #0d1c2b;
  --text-muted: #51607a;
  --primary: #0c4587;
  --primary-dark: #083366;
  --primary-tint: #e7eef8;
  --accent: #055138;
  --accent-tint: #e6f4ed;
  --warn: #7a4300;
  --warn-tint: #fff3dc;
  --warn-border: #f0b44c;
  --danger: #a3141c;
  --danger-tint: #fdecec;
  --radius-sm: 8px;
  --radius: 16px;
  --radius-pill: 9999px;
  --shadow-sm: 0 4px 12px rgba(10, 22, 40, .08);
  --font: "DM Sans", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial,
    "Noto Sans", sans-serif;
}
*, *::before, *::after { box-sizing: border-box; }
[hidden] { display: none !important; }
html { scroll-behavior: smooth; }
body {
  margin: 0; font-family: var(--font); font-size: 16px; line-height: 1.55;
  color: var(--text); background: var(--surface-light); overflow-wrap: anywhere;
}
a { color: var(--primary); }
a:hover { color: var(--primary-dark); }
a:focus-visible, button:focus-visible { outline: 3px solid var(--primary); outline-offset: 2px; }
.wrap { max-width: 980px; margin: 0 auto; padding: 0 20px; }

.hero {
  color: #fff;
  background: linear-gradient(180deg, var(--navy-950) 0%, var(--navy-900) 60%, var(--primary) 100%);
  padding: 32px 0 40px;
}
.product {
  display: inline-block; padding: 4px 12px; border-radius: var(--radius-pill);
  background: #fff; color: var(--navy-950); font-size: .8125rem; font-weight: 600; letter-spacing: .02em;
}
.hero h1 { margin: 16px 0 8px; font-size: clamp(1.75rem, 4.5vw, 2.75rem); font-weight: 700;
  line-height: 1.1; letter-spacing: -.02em; }
.meta { margin: 0; color: rgba(255, 255, 255, .86); }
.meta code { font-family: inherit; font-weight: 600; color: #fff; }
.stats { display: flex; flex-wrap: wrap; gap: 8px; margin: 20px 0 0; padding: 0; list-style: none; }
.stats li {
  padding: 6px 14px; border-radius: var(--radius-pill); font-size: .9375rem;
  background: rgba(255, 255, 255, .1); border: 1px solid rgba(255, 255, 255, .22);
}
.stats strong { font-weight: 700; }
.stats li.stat-warn { background: var(--warn-tint); color: var(--warn); border-color: var(--warn-border); }
.notice {
  margin: 24px 0 0; padding: 14px 18px; border-radius: var(--radius);
  background: var(--accent-tint); color: var(--accent); font-weight: 600;
  border-left: 6px solid var(--accent); box-shadow: var(--shadow-sm);
}
.note-warn {
  margin: 12px 0 0; padding: 12px 18px; border-radius: var(--radius);
  background: var(--warn-tint); color: var(--warn); border-left: 6px solid var(--warn-border);
}

.nav {
  position: sticky; top: 0; z-index: 10; background: rgba(255, 255, 255, .96);
  border-bottom: 1px solid var(--border); box-shadow: var(--shadow-sm);
}
.nav ul { display: flex; flex-wrap: wrap; gap: 0 2px; margin: 0 auto; padding: 6px 12px;
  list-style: none; max-width: 980px; }
.nav a {
  display: block; white-space: nowrap; padding: 3px 8px; border-radius: var(--radius-pill);
  color: var(--navy-700); text-decoration: none; font-size: .8125rem; font-weight: 500;
}
.nav a:hover { background: var(--surface-mid); color: var(--navy-950); }

main { padding: 8px 0 48px; }
section { margin-top: 40px; scroll-margin-top: 88px; }
h2 { margin: 0 0 6px; font-size: 1.5rem; font-weight: 700; letter-spacing: -.01em; color: var(--navy-950); }
.target { margin: 0 0 16px; color: var(--text-muted); font-size: .9375rem; }
.lead { margin: 12px 0 0; font-size: 1.0625rem; max-width: 72ch; }
.empty { margin: 16px 0 0; font-weight: 700; }

.cards { display: grid; gap: 14px; margin-top: 16px; }
.card {
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  box-shadow: var(--shadow-sm); padding: 18px 20px; scroll-margin-top: 88px;
}
.card h3 { margin: 0; font-size: 1.125rem; font-weight: 700; line-height: 1.35; color: var(--navy-950); }
.card-id { color: var(--primary); margin-right: 6px; }
.card.needs-review { border-left: 6px solid var(--warn-border); }
/* After needs-review on purpose: a prohibition keeps its red edge even when its evidence is weak. */
.card.do-not-do { border-left: 6px solid var(--danger); }
.card p { margin: 10px 0 0; }

.badges { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
.badge {
  display: inline-block; padding: 2px 10px; border-radius: var(--radius-pill); font-size: .8125rem;
  font-weight: 600; border: 1px solid transparent; line-height: 1.6;
}
.badge-kind { background: var(--surface); color: var(--navy-700); border-color: #b9c4d3; }
.state-do_now { background: var(--primary-tint); color: var(--primary); }
.state-scheduled { background: #ece9fb; color: #3f2c96; }
.state-waiting_on_client { background: var(--warn-tint); color: var(--warn); }
.state-on_hold { background: var(--surface-mid); color: #3b4a5f; }
.state-do_not_do { background: var(--danger); color: #fff; }
.state-no_action { background: #f1f2f4; color: #4a5160; }
.flag {
  display: inline-block; margin-left: 6px; padding: 1px 10px; border-radius: var(--radius-pill);
  background: var(--warn-tint); color: var(--warn); border: 1px solid var(--warn-border);
  font-size: .8125rem; font-weight: 700; vertical-align: middle;
}

.facts { display: grid; grid-template-columns: 9.5rem 1fr; gap: 4px 14px; margin: 14px 0 0;
  font-size: .9375rem; }
.facts dt { color: var(--text-muted); font-weight: 600; }
.facts dd { margin: 0; }
.facts ul { margin: 0; padding-left: 1.1em; }

.quotes { margin: 14px 0 0; padding: 0; list-style: none; display: grid; gap: 8px; }
.quote {
  margin: 0; padding: 8px 12px; border-radius: var(--radius-sm); background: var(--surface-light);
  border-left: 3px solid #b9c4d3; font-size: .9375rem;
}
.quote-meta { display: block; font-size: .8125rem; color: var(--text-muted); }
.quote-meta strong { color: var(--navy-700); }
.quote.unverified { border-left-color: var(--warn-border); background: var(--warn-tint); }
.quote.unverified .quote-meta { color: var(--warn); }
.quote.missing { color: var(--warn); background: var(--warn-tint); border-left-color: var(--warn-border); }

.guard-meta { margin: 8px 0 0; font-size: .9375rem; color: var(--text-muted); }
.guard-meta strong { color: var(--text); }

.issues { margin: 16px 0 0; padding: 0; list-style: none; display: grid; gap: 8px; }
.issues li { padding: 10px 14px; border-radius: var(--radius-sm); background: var(--warn-tint);
  color: var(--warn); border: 1px solid var(--warn-border); }

.timeline { margin: 16px 0 0; padding: 0; list-style: none; background: var(--surface);
  border: 1px solid var(--border); border-radius: var(--radius); box-shadow: var(--shadow-sm); }
.timeline li { display: grid; grid-template-columns: 7.5rem 1fr; gap: 4px 16px; padding: 12px 20px;
  border-top: 1px solid var(--surface-mid); }
.timeline li:first-child { border-top: 0; }
.timeline time { font-weight: 700; color: var(--primary); font-variant-numeric: tabular-nums; }
.timeline .limits { display: block; color: var(--text-muted); font-size: .875rem; }

.filter { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin-top: 24px; }
.filter span { font-weight: 600; margin-right: 4px; }
.filter button {
  font: inherit; font-size: .875rem; padding: 4px 12px; border-radius: var(--radius-pill); cursor: pointer;
  background: var(--surface); color: var(--navy-700); border: 1px solid #b9c4d3;
}
.filter button[aria-pressed="true"] { background: var(--primary); border-color: var(--primary); color: #fff; }

.draft-body {
  margin: 14px 0 0; padding: 14px 16px; border-radius: var(--radius-sm); background: var(--surface-light);
  border: 1px solid var(--border); white-space: pre-wrap; font-family: inherit; font-size: .9375rem;
}
.draft-file { margin: 10px 0 0; font-size: .875rem; }

.assumptions { margin: 16px 0 0; padding-left: 1.2em; }
.assumptions li { margin-top: 6px; }

@media (max-width: 560px) {
  .wrap { padding: 0 16px; }
  /* One swipeable row instead of a nav block that would cover half of a phone screen. */
  .nav ul { flex-wrap: nowrap; overflow-x: auto; scrollbar-width: none; padding: 8px 16px; }
  section, .card { scroll-margin-top: 64px; }
  .card { padding: 16px; }
  .facts { grid-template-columns: 1fr; gap: 0; }
  .facts dd { margin-bottom: 8px; }
  .timeline li { grid-template-columns: 1fr; padding: 12px 16px; }
}
"""

# Progressive enhancement: without JS the filter stays hidden and every item is shown.
SCRIPT = """
const bar = document.querySelector('.filter');
if (bar) {
  bar.hidden = false;
  bar.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-state]');
    if (!button) return;
    const state = button.dataset.state;
    bar.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', String(b === button)));
    document.querySelectorAll('article.item').forEach((card) => {
      card.hidden = state !== '' && card.dataset.state !== state;
    });
    document.querySelectorAll('section.inbox').forEach((section) => {
      section.hidden = !section.querySelector('article.item:not([hidden])');
    });
  });
}
"""


def esc(value: object) -> str:
    return escape(str(value), quote=True)


def render_html(routed: RoutedMeeting, report: VerificationReport, source_name: str) -> str:
    extraction = routed.extraction
    title = f"Po rozmowie: {extraction.client}, {extraction.meeting_date or 'data nieznana'}"
    body = [
        render_header(routed, report, source_name, title),
        render_nav(routed, report),
        '<main class="wrap">',
        render_summary(routed),
        render_guardrails(extraction.guardrails, report),
        render_issues(report),
        render_calendar(routed.calendar),
        render_state_filter(extraction.items),
        *(render_inbox(inbox, routed.inboxes[inbox], report) for inbox in INBOX_ORDER),
        render_drafts(extraction.drafts),
        render_assumptions(extraction.assumptions),
        "</main>",
    ]
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="pl">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{esc(title)} · callflow</title>",
            FONT_LINK,
            f"<style>{STYLE}</style>",
            "</head>",
            "<body>",
            *(part for part in body if part),
            f"<script>{SCRIPT}</script>",
            "</body>",
            "</html>",
            "",
        ]
    )


def render_header(routed: RoutedMeeting, report: VerificationReport, source_name: str, title: str) -> str:
    extraction = routed.extraction
    verified = sum(check.verified for check in report.quotes)
    quotes_class = ' class="stat-warn"' if verified < len(report.quotes) else ""
    stats = [
        f"<li>Pozycji: <strong>{len(extraction.items)}</strong></li>",
        f"<li>Zabezpieczeń: <strong>{len(extraction.guardrails)}</strong></li>",
        f"<li>Szkiców: <strong>{len(extraction.drafts)}</strong></li>",
        f"<li{quotes_class}>Cytaty zweryfikowane: <strong>{verified}/{len(report.quotes)}</strong></li>",
    ]
    participants = esc(", ".join(extraction.participants))
    missing_date = ""
    if extraction.meeting_date is None:
        missing_date = f'<p class="note-warn" role="note">{esc(MISSING_DATE_NOTE.removeprefix("> "))}</p>'
    return f"""<header class="hero">
<div class="wrap">
<span class="product">callflow</span>
<h1>{esc(title)}</h1>
<p class="meta">Źródło: <code>{esc(source_name)}</code> · uczestnicy: {participants}</p>
<ul class="stats" aria-label="Statystyki">{"".join(stats)}</ul>
<p class="notice" role="note">{esc(NO_CHANGES_NOTICE)}</p>
{missing_date}
</div>
</header>"""


def _nav_label(inbox: Inbox) -> str:
    return re.split(r" \(|:", inbox.value)[0]


def render_nav(routed: RoutedMeeting, report: VerificationReport) -> str:
    extraction = routed.extraction
    links = [("summary", "Podsumowanie")]
    if extraction.guardrails:
        links.append(("guardrails", f"Zabezpieczenia ({len(extraction.guardrails)})"))
    if report.issues:
        links.append(("issues", f"Ostrzeżenia ({len(report.issues)})"))
    if routed.calendar:
        links.append(("calendar", "Terminy"))
    for inbox in INBOX_ORDER:
        if routed.inboxes[inbox]:
            links.append((f"inbox-{inbox.name}", f"{_nav_label(inbox)} ({len(routed.inboxes[inbox])})"))
    if extraction.drafts:
        links.append(("drafts", f"Szkice ({len(extraction.drafts)})"))
    if extraction.assumptions:
        links.append(("assumptions", "Założenia"))
    items = "".join(f'<li><a href="#{anchor}">{esc(label)}</a></li>' for anchor, label in links)
    return f'<nav class="nav" aria-label="Sekcje raportu"><ul>{items}</ul></nav>'


def render_summary(routed: RoutedMeeting) -> str:
    extraction = routed.extraction
    empty = ""
    if not extraction.items and not extraction.guardrails:
        empty = f'<p class="empty">{esc(EMPTY_CALL_NOTE)}</p>'
    return f"""<section id="summary">
<h2>Podsumowanie</h2>
<p class="lead">{esc(extraction.summary)}</p>
{empty}
</section>"""


def render_evidence(owner_id: str, evidence: list[Evidence], report: VerificationReport) -> str:
    quotes = []
    for check in report.quotes_for(owner_id):
        where = f"l. {check.line}" if check.line else "brak w transkrypcji"
        mark = "✅" if check.verified else "⚠️ niezweryfikowany"
        css = "quote" if check.verified else "quote unverified"
        quotes.append(
            f'<li><blockquote class="{css}"><span class="quote-meta"><strong>{esc(check.speaker)}</strong>'
            f" ({where}) {mark}</span>„{esc(check.quote)}”</blockquote></li>"
        )
    if not evidence:
        quotes.append('<li><p class="quote missing">⚠️ brak cytatu</p></li>')
    return f'<ul class="quotes" aria-label="Cytaty">{"".join(quotes)}</ul>'


def render_guardrails(guardrails: list[Guardrail], report: VerificationReport) -> str:
    if not guardrails:
        return ""
    cards = []
    for index, guardrail in enumerate(guardrails, 1):
        guardrail_id = f"G{index:02d}"
        details = [
            f"<strong>do:</strong> {esc(guardrail.until)}" if guardrail.until else "",
            f"<strong>zdejmuje:</strong> {esc(guardrail.approval_by)}" if guardrail.approval_by else "",
        ]
        meta = " · ".join(part for part in details if part)
        cards.append(
            f'<article class="card guardrail" id="{guardrail_id}">'
            f'<h3><span class="card-id">{guardrail_id}</span>{esc(guardrail.rule)}</h3>'
            + (f'<p class="guard-meta">{meta}</p>' if meta else "")
            + render_evidence(guardrail_id, guardrail.evidence, report)
            + "</article>"
        )
    return f"""<section id="guardrails">
<h2>Zabezpieczenia (sprawdzić przed każdym działaniem)</h2>
<div class="cards">{"".join(cards)}</div>
</section>"""


def render_issues(report: VerificationReport) -> str:
    if not report.issues:
        return ""
    rows = "".join(
        f"<li><strong>{esc(issue.owner_id)}</strong>: {esc(issue.message)}</li>" for issue in report.issues
    )
    return f"""<section id="issues">
<h2>Ostrzeżenia walidacji</h2>
<ul class="issues">{rows}</ul>
</section>"""


def render_calendar(calendar: list[ActionItem]) -> str:
    if not calendar:
        return ""
    rows = []
    for item in calendar:
        limits = f'<span class="limits">{esc("; ".join(item.constraints))}</span>' if item.constraints else ""
        rows.append(
            f'<li><time datetime="{item.due_date}">{item.due_date}</time>'
            f'<div><a href="#{esc(item.id)}">{esc(item.id)}</a> {esc(item.title)}{limits}</div></li>'
        )
    return f"""<section id="calendar">
<h2>Terminy (kalendarz i przypomnienia)</h2>
<ol class="timeline">{"".join(rows)}</ol>
</section>"""


def render_state_filter(items: list[ActionItem]) -> str:
    present = {item.state for item in items}
    states = [state for state in State if state in present]
    if len(states) < 2:
        return ""
    buttons = ['<button type="button" data-state="" aria-pressed="true">wszystkie</button>']
    buttons += [
        f'<button type="button" data-state="{state.value}" aria-pressed="false">{state.value}</button>'
        for state in states
    ]
    return (
        '<div class="filter" role="group" aria-label="Filtr pozycji wg stanu" hidden>'
        f"<span>Stan:</span>{''.join(buttons)}</div>"
    )


def render_inbox(inbox: Inbox, items: list[ActionItem], report: VerificationReport) -> str:
    if not items:
        return ""
    cards = "".join(render_item(item, report) for item in items)
    return f"""<section class="inbox" id="inbox-{inbox.name}">
<h2>{esc(inbox.value)}</h2>
<p class="target">Cel: {esc(TARGET_SYSTEM[inbox])}</p>
<div class="cards">{cards}</div>
</section>"""


def render_item(item: ActionItem, report: VerificationReport) -> str:
    needs_review = item.id in report.unverified_ids()
    classes = ["card", "item"]
    if item.state == State.do_not_do:
        classes.append("do-not-do")
    if needs_review:
        classes.append("needs-review")
    flag = '<span class="flag">⚠️ do sprawdzenia</span>' if needs_review else ""
    return (
        f'<article class="{" ".join(classes)}" id="{esc(item.id)}" data-state="{item.state.value}">'
        f'<h3><span class="card-id">{esc(item.id)}</span>{esc(item.title)}{flag}</h3>'
        f'<div class="badges"><span class="badge badge-kind">{item.kind.value}</span>'
        f'<span class="badge state-{item.state.value}">{item.state.value}</span></div>'
        f"<p>{esc(item.details)}</p>"
        f"{render_facts(item)}"
        f"{render_evidence(item.id, item.evidence, report)}"
        "</article>"
    )


def render_facts(item: ActionItem) -> str:
    facts = [
        ("Właściciel", esc(item.owner) if item.owner else ""),
        ("Termin", esc(_due(item) or "")),
        ("Warunek", esc(item.condition) if item.condition else ""),
        ("Zatwierdza", esc(item.approval_by) if item.approval_by else ""),
        ("Wersja ostateczna", esc(item.final_value) if item.final_value else ""),
        ("Zastępuje", _list(item.superseded)),
        ("Ograniczenia", _list(item.constraints)),
        ("Zależy od", _refs(item.depends_on)),
    ]
    rows = "".join(f"<dt>{label}</dt><dd>{value}</dd>" for label, value in facts if value)
    return f'<dl class="facts">{rows}</dl>' if rows else ""


def _refs(item_ids: list[str]) -> str:
    return ", ".join(f'<a href="#{esc(item_id)}">{esc(item_id)}</a>' for item_id in item_ids)


def _list(values: list[str]) -> str:
    if not values:
        return ""
    if len(values) == 1:
        return esc(values[0])
    return "<ul>" + "".join(f"<li>{esc(value)}</li>" for value in values) + "</ul>"


def render_drafts(drafts: list[Draft]) -> str:
    if not drafts:
        return ""
    cards = []
    for index, (draft, path) in enumerate(zip(drafts, draft_paths(drafts), strict=True), 1):
        cards.append(
            f'<article class="card draft" id="D{index:02d}">'
            f'<h3><span class="card-id">D{index:02d}</span>{esc(draft.subject)}</h3>'
            f'<dl class="facts"><dt>Do</dt><dd>{esc(draft.to)}</dd>'
            f"<dt>Temat</dt><dd>{esc(draft.subject)}</dd>"
            f"<dt>Wysłać</dt><dd>{esc(draft.send_when)}</dd>"
            f"<dt>Dotyczy</dt><dd>{_refs(draft.related_items)}</dd></dl>"
            f'<div class="draft-body">{esc(draft.body)}</div>'
            f'<p class="draft-file">Plik: <a href="{esc(path)}">{esc(path)}</a></p>'
            "</article>"
        )
    return f"""<section id="drafts">
<h2>Szkice wiadomości (do zatwierdzenia)</h2>
<div class="cards">{"".join(cards)}</div>
</section>"""


def render_assumptions(assumptions: list[str]) -> str:
    if not assumptions:
        return ""
    rows = "".join(f"<li>{esc(assumption)}</li>" for assumption in assumptions)
    return f"""<section id="assumptions">
<h2>Założenia przyjęte przy analizie</h2>
<ul class="assumptions">{rows}</ul>
</section>"""
