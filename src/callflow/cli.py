"""Command line entry point: transcript in, verified and routed follow-up actions out."""

from __future__ import annotations

import argparse
import sys
import time
from datetime import date
from pathlib import Path

from pydantic import ValidationError

from callflow import llm
from callflow.extract import ExtractionError, extract
from callflow.html_report import render_html
from callflow.render import REPORT_FILE, write_json, write_outputs
from callflow.route import route
from callflow.schema import MeetingExtraction
from callflow.transcript import parse_transcript
from callflow.verify import verify

EXTRACTION_FILE = "extraction.json"
RAW_RESPONSE_FILE = "raw_response.json"
HTML_REPORT_FILE = "report.html"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="callflow", description="Turn a client call transcript into verified follow-up actions."
    )
    parser.add_argument("transcript", type=Path, help="markdown/text transcript of the call")
    parser.add_argument("--out", type=Path, required=True, help="output directory")
    parser.add_argument(
        "--from-json",
        type=Path,
        metavar="EXTRACTION",
        help="skip the model and use a saved extraction.json (offline, no Claude needed)",
    )
    parser.add_argument("--meeting-date", type=date.fromisoformat, help="YYYY-MM-DD, overrides the header")
    parser.add_argument("--vendor", default="Rinvo", help="company on whose behalf actions are prepared")
    parser.add_argument("--model", default=llm.DEFAULT_MODEL)
    parser.add_argument("--effort", default=llm.DEFAULT_EFFORT, choices=["low", "medium", "high", "xhigh"])
    return parser


def main(argv: list[str] | None = None) -> int:
    # Windows consoles and pipes default to a legacy code page; the report text is Polish.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except (llm.LLMError, ExtractionError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


def run(args: argparse.Namespace) -> int:
    transcript_text = args.transcript.read_text(encoding="utf-8-sig")
    transcript = parse_transcript(transcript_text, source=args.transcript.name)
    if not transcript.turns:
        raise ValueError(
            f"no speaker turns found in {args.transcript}; "
            "expected lines like '**Name:** text' or 'Name: text'"
        )

    if args.from_json:
        extraction = load_extraction(args.from_json)
    else:
        extraction = extract_and_save(args, transcript_text, transcript.call_date)

    report = verify(extraction, transcript)
    unverified = report.unverified_ids()
    print(
        f"{len(extraction.items)} items, {len(extraction.guardrails)} guardrails, "
        f"{len(extraction.drafts)} drafts; {len(report.quotes)} quotes, "
        f"{len(unverified)} with unverified evidence; {len(report.issues)} issues"
    )
    for issue in report.issues:
        print(f"  [{issue.owner_id}] {issue.message}")
    routed = route(extraction)
    write_outputs(routed, report, args.out, args.transcript.name)
    html = render_html(routed, report, args.transcript.name)
    (args.out / HTML_REPORT_FILE).write_text(html, encoding="utf-8")
    print(f"Report: {args.out / REPORT_FILE} and {args.out / HTML_REPORT_FILE}")
    return 0


def extract_and_save(
    args: argparse.Namespace, transcript_text: str, call_date: str | None
) -> MeetingExtraction:
    """Run the model and save its raw response (also when validation fails) and the extraction."""
    meeting_date = args.meeting_date or (date.fromisoformat(call_date) if call_date else None)
    if meeting_date is None:
        print(
            "warning: meeting date not found in the transcript; relative deadlines will not be "
            "resolved (pass --meeting-date YYYY-MM-DD to fix)",
            file=sys.stderr,
        )
    print(f"Extracting with {args.model} (effort {args.effort}); this takes a few minutes...")
    started = time.monotonic()
    args.out.mkdir(parents=True, exist_ok=True)
    try:
        extraction, raw = extract(
            transcript_text, meeting_date, args.vendor, model=args.model, effort=args.effort
        )
    except ExtractionError as exc:
        if exc.raw is not None:
            write_json(args.out / RAW_RESPONSE_FILE, exc.raw)
        raise
    write_json(args.out / RAW_RESPONSE_FILE, raw)
    write_json(args.out / EXTRACTION_FILE, extraction.model_dump(mode="json"))
    cost = raw.get("total_cost_usd")
    cost_text = f"${cost:.2f}" if isinstance(cost, int | float) else "unknown"
    print(f"Done in {time.monotonic() - started:.0f} s, cost {cost_text}")
    return extraction


def load_extraction(path: Path) -> MeetingExtraction:
    try:
        return MeetingExtraction.model_validate_json(path.read_text(encoding="utf-8"))
    except ValidationError as exc:
        raise ValueError(f"{path} is not a valid extraction: {exc}") from exc


if __name__ == "__main__":
    raise SystemExit(main())
