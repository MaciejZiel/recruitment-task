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
from callflow.jira import JiraConfig, JiraError, check_connection, load_dotenv, push_to_jira
from callflow.render import REPORT_FILE, write_json, write_outputs
from callflow.route import route
from callflow.schema import MeetingExtraction
from callflow.transcript import parse_transcript
from callflow.verify import verify

EXTRACTION_FILE = "extraction.json"
RAW_RESPONSE_FILE = "raw_response.json"
HTML_REPORT_FILE = "report.html"
DOTENV_FILE = Path(".env")


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
    parser.add_argument(
        "--jira",
        action="store_true",
        help="create Jira issues for verified bugs and agent config changes (settings in .env)",
    )
    parser.add_argument(
        "--jira-check",
        action="store_true",
        help="before the run, check Jira login, project and issue types (creates nothing)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    # Windows consoles and pipes default to a legacy code page; the report text is Polish.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except (llm.LLMError, ExtractionError, JiraError, ValueError, OSError) as exc:
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

    # Jira settings are read before the model call so a mistake there costs nothing.
    jira_config = None
    if args.jira or args.jira_check:
        load_dotenv(DOTENV_FILE)
        jira_config = JiraConfig.from_env()
    if args.jira_check and jira_config and not report_jira_check(jira_config):
        return 1

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

    if args.jira and jira_config:
        result = push_to_jira(routed, report, args.out, jira_config)
        for item_id, key in result.created.items():
            print(f"Jira: created {key} for {item_id} ({jira_config.base_url}/browse/{key})")
        for item_id, reason in result.skipped:
            print(f"Jira: skipped {item_id} ({reason})")
        print(f"Jira: {len(result.created)} created, {len(result.skipped)} skipped")
    return 0


def report_jira_check(config: JiraConfig) -> bool:
    check = check_connection(config)
    print(f"Jira: authenticated as {check.user} at {config.base_url}")
    print(f"Jira: project {check.project} found; issue types: {', '.join(check.issue_types) or 'none'}")
    for label, name in (("bugs", config.issue_type_bug), ("config changes", config.issue_type_config)):
        status = "OK" if name in check.issue_types else "MISSING"
        print(f"Jira: issue type for {label}: {name} {status}")
    for problem in check.problems:
        print(f"Jira problem: {problem}", file=sys.stderr)
    return not check.problems


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
