"""Deterministic checks of a model extraction against the transcript it came from."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import date

from callflow.schema import Evidence, MeetingExtraction, State
from callflow.transcript import Transcript

_CHAR_MAP = str.maketrans({"„": '"', "”": '"', "“": '"', "«": '"', "»": '"', "’": "'", "–": "-", "—": "-"})
_WHITESPACE_RE = re.compile(r"\s+")


def normalize(text: str) -> str:
    text = text.replace("**", "").translate(_CHAR_MAP)
    return _WHITESPACE_RE.sub(" ", text).strip().lower()


@dataclass
class QuoteCheck:
    owner_id: str
    speaker: str
    quote: str
    line: int | None
    speaker_matches: bool

    @property
    def verified(self) -> bool:
        return self.line is not None and self.speaker_matches


@dataclass
class Issue:
    owner_id: str
    message: str


@dataclass
class VerificationReport:
    quotes: list[QuoteCheck] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)

    def unverified_ids(self) -> set[str]:
        return {check.owner_id for check in self.quotes if not check.verified}

    def quotes_for(self, owner_id: str) -> list[QuoteCheck]:
        return [check for check in self.quotes if check.owner_id == owner_id]


def check_quote(owner_id: str, evidence: Evidence, transcript: Transcript) -> QuoteCheck:
    needle = normalize(evidence.quote)
    matches = [turn for turn in transcript.turns if needle and needle in normalize(turn.text)]
    same_speaker = [turn for turn in matches if normalize(turn.speaker) == normalize(evidence.speaker)]
    best = (same_speaker or matches or [None])[0]
    return QuoteCheck(
        owner_id=owner_id,
        speaker=evidence.speaker,
        quote=evidence.quote,
        line=best.line if best else None,
        speaker_matches=bool(same_speaker),
    )


def verify(extraction: MeetingExtraction, transcript: Transcript) -> VerificationReport:
    report = VerificationReport()
    item_ids = [item.id for item in extraction.items]
    known_ids = set(item_ids)

    for item_id, count in Counter(item_ids).items():
        if count > 1:
            report.issues.append(Issue(item_id, f"id występuje {count} razy"))

    evidenced = [(item.id, item.evidence) for item in extraction.items] + [
        (f"G{index:02d}", guardrail.evidence) for index, guardrail in enumerate(extraction.guardrails, 1)
    ]
    for owner_id, evidence_list in evidenced:
        if not evidence_list:
            report.issues.append(Issue(owner_id, "brak cytatu-dowodu"))
        for evidence in evidence_list:
            check = check_quote(owner_id, evidence, transcript)
            report.quotes.append(check)
            if check.line is None:
                report.issues.append(
                    Issue(owner_id, f"cytat nie występuje w transkrypcji: {evidence.quote!r}")
                )
            elif not check.speaker_matches:
                report.issues.append(
                    Issue(owner_id, f"cytat z linii {check.line} nie pochodzi od {evidence.speaker!r}")
                )

    for item in extraction.items:
        report.issues.extend(_check_item_fields(item, extraction.meeting_date, known_ids))

    for index, draft in enumerate(extraction.drafts, 1):
        draft_id = f"D{index:02d}"
        if not draft.related_items:
            report.issues.append(Issue(draft_id, "szkic nie jest powiązany z żadną pozycją"))
        for related in draft.related_items:
            if related not in known_ids:
                report.issues.append(Issue(draft_id, f"powiązanie z nieistniejącą pozycją {related}"))

    return report


def _check_item_fields(item, meeting_date: date, known_ids: set[str]) -> list[Issue]:
    issues = []
    if item.due_date and item.due_date < meeting_date:
        issues.append(Issue(item.id, f"termin {item.due_date} jest przed datą spotkania"))
    if item.state in (State.do_now, State.scheduled) and not item.owner:
        issues.append(Issue(item.id, "pozycja do wykonania bez właściciela"))
    if item.state == State.scheduled and not item.due_date:
        issues.append(Issue(item.id, "stan 'scheduled' bez terminu"))
    for dependency in item.depends_on:
        if dependency not in known_ids:
            issues.append(Issue(item.id, f"zależność od nieistniejącej pozycji {dependency}"))
    return issues
