"""Parse a markdown call transcript into a structured, line-addressable form."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

POLISH_MONTHS_GENITIVE = {
    "stycznia": 1,
    "lutego": 2,
    "marca": 3,
    "kwietnia": 4,
    "maja": 5,
    "czerwca": 6,
    "lipca": 7,
    "sierpnia": 8,
    "września": 9,
    "października": 10,
    "listopada": 11,
    "grudnia": 12,
}

DATE_RE = re.compile(r"\b(\d{1,2})\s+(" + "|".join(POLISH_MONTHS_GENITIVE) + r")\s+(\d{4})\b", re.IGNORECASE)
ISO_DATE_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
DOTTED_DATE_RE = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b")
# "**Kasia:** text" and the variant "**Kasia**: text".
TURN_RE = re.compile(r"^\*\*(?P<speaker>[^*]+?)(?::\*\*|\*\*:)\s*(?P<text>.+)$")
# Fallback for transcripts without bold labels: "Kasia: ..." or "[00:01:02] Speaker 1: ...".
PLAIN_TURN_RE = re.compile(r"^(?:\[[\d:.]+\]\s*)?(?P<speaker>[A-ZĄĆĘŁŃÓŚŹŻ][^:*\[\]]{0,39}):\s+(?P<text>.+)$")
STAGE_RE = re.compile(r"^\*(?P<text>\[.+)\*$")
PARTICIPANT_RE = re.compile(r"^-\s+\*\*(?P<name>[^*]+)\*\*,\s*(?P<rest>.+)$")


@dataclass
class Turn:
    line: int
    speaker: str
    text: str


@dataclass
class StageDirection:
    line: int
    text: str


@dataclass
class Participant:
    name: str
    details: str


@dataclass
class Transcript:
    source: str
    title: str | None
    call_date: str | None
    header_lines: list[str] = field(default_factory=list)
    sections: dict[str, list[str]] = field(default_factory=dict)
    participants: list[Participant] = field(default_factory=list)
    turns: list[Turn] = field(default_factory=list)
    stage_directions: list[StageDirection] = field(default_factory=list)


def parse_call_date(text: str) -> date | None:
    """Return the first valid date in the text, whichever of the supported formats it uses."""
    candidates: list[tuple[int, int, int, int]] = []
    for match in ISO_DATE_RE.finditer(text):
        year, month, day = map(int, match.groups())
        candidates.append((match.start(), year, month, day))
    for match in DATE_RE.finditer(text):
        day, month_name, year = match.groups()
        candidates.append((match.start(), int(year), POLISH_MONTHS_GENITIVE[month_name.lower()], int(day)))
    for match in DOTTED_DATE_RE.finditer(text):
        day, month, year = map(int, match.groups())
        candidates.append((match.start(), year, month, day))
    for _, year, month, day in sorted(candidates):
        try:
            return date(year, month, day)
        except ValueError:
            continue
    return None


def _is_transcript_heading(line: str) -> bool:
    return line.startswith("## ") and line[3:].strip().lower().startswith(("transkrypcja", "transcript"))


def parse_transcript(text: str, source: str = "<string>") -> Transcript:
    lines = text.removeprefix("﻿").splitlines()
    title = None
    call_date = None
    header_lines: list[str] = []
    sections: dict[str, list[str]] = {}
    participants: list[Participant] = []
    turns: list[Turn] = []
    stage_directions: list[StageDirection] = []
    plain_turns: list[Turn] = []
    current_section: str | None = None
    # Bold "**Label:**" lines also appear in context sections (e.g. a glossary), so when the
    # file has a dedicated transcript section, only lines inside it count as speaker turns.
    has_transcript_section = any(_is_transcript_heading(line.strip()) for line in lines)

    for number, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# ") and title is None:
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            current_section = line[3:].strip()
            sections.setdefault(current_section, [])
            continue

        in_dialogue = not has_transcript_section or _is_transcript_heading(f"## {current_section}")
        if in_dialogue and (match := TURN_RE.match(line)):
            turns.append(Turn(number, match["speaker"].strip(), match["text"].strip()))
            continue
        if match := STAGE_RE.match(line):
            stage_directions.append(StageDirection(number, match["text"].strip()))
            continue
        if in_dialogue and turns:
            # A line that starts no new turn continues the previous utterance (wrapped text, paragraphs).
            turns[-1].text += " " + line
            continue
        if in_dialogue and (match := PLAIN_TURN_RE.match(line)):
            plain_turns.append(Turn(number, match["speaker"].strip(), match["text"].strip()))
            continue
        if in_dialogue and plain_turns:
            plain_turns[-1].text += " " + line
            continue

        if current_section is None:
            header_lines.append(line)
            if call_date is None and (found := parse_call_date(line)):
                call_date = found.isoformat()
            continue

        sections[current_section].append(line)
        if current_section.lower().startswith("uczestnicy") and (match := PARTICIPANT_RE.match(line)):
            participants.append(Participant(match["name"].strip(), match["rest"].strip()))

    return Transcript(
        source=source,
        title=title,
        call_date=call_date,
        header_lines=header_lines,
        sections=sections,
        participants=participants,
        turns=turns or plain_turns,
        stage_directions=stage_directions,
    )


def load_transcript(path: Path) -> Transcript:
    return parse_transcript(path.read_text(encoding="utf-8-sig"), source=path.name)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert a markdown call transcript to JSON.")
    parser.add_argument("transcript", type=Path)
    parser.add_argument("-o", "--output", type=Path, help="output JSON path (default: stdout)")
    args = parser.parse_args(argv)

    transcript = load_transcript(args.transcript)
    if not transcript.turns:
        print(f"error: no speaker turns found in {args.transcript}", file=sys.stderr)
        return 1

    payload = json.dumps(asdict(transcript), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
