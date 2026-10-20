"""Run the callflow pipeline for web requests: validation, a background worker and run storage."""

from __future__ import annotations

import json
import logging
import queue
import re
import secrets
import threading
import time
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

from callflow import llm
from callflow.cli import EXTRACTION_FILE, HTML_REPORT_FILE, RAW_RESPONSE_FILE, load_extraction
from callflow.extract import ExtractionError, extract
from callflow.html_report import render_html
from callflow.render import OUTBOX_FILE, REPORT_FILE, build_outbox, write_json, write_outputs
from callflow.route import route
from callflow.schema import MeetingExtraction
from callflow.transcript import Transcript, parse_transcript
from callflow.verify import VerificationReport, verify

log = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[3]
EXAMPLES_DIR = REPO_ROOT / "examples"
TRANSCRIPT_FILE = "transcript.md"
RUN_FILE = "run.json"
RESULT_FILE = "result.json"

MAX_TRANSCRIPT_BYTES = 300 * 1024
MAX_SOURCE_NAME = 200
MAX_VENDOR = 100
EFFORTS = ("low", "medium", "high")
MODES = ("live", "example")
RUN_ID_PATTERN = r"\d{8}-\d{6}-[0-9a-f]{4}"
_ISO_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

# (id, transcript, saved extraction), relative to EXAMPLES_DIR.
EXAMPLE_SPECS = (
    ("auto-tama", "transkrypcja-spotkanie.md", "output/auto-tama/extraction.json"),
    ("dentavita", "druga-rozmowa.md", "output/dentavita/extraction.json"),
    ("fitstudio", "synthetic/fitstudio-rozmowa.md", "output/fitstudio/extraction.json"),
)


class RequestError(ValueError):
    """Invalid run request; the message is shown to the user."""


class BusyError(RuntimeError):
    """A live run is refused while another one is queued or running."""


class ResultFileError(RuntimeError):
    """The result.json of a finished run cannot be read."""


@dataclass(frozen=True)
class Example:
    id: str
    transcript_path: Path
    extraction_path: Path

    def to_json(self) -> dict[str, Any]:
        text = self.transcript_path.read_text(encoding="utf-8-sig")
        return {
            "id": self.id,
            "title": parse_transcript(text).title or self.id,
            "transcript_name": self.transcript_path.name,
            "transcript": text,
        }


def find_examples(examples_dir: Path | None = None) -> dict[str, Example]:
    base = examples_dir or EXAMPLES_DIR
    found = {}
    for example_id, transcript, extraction in EXAMPLE_SPECS:
        example = Example(example_id, base / transcript, base / extraction)
        if example.transcript_path.is_file() and example.extraction_path.is_file():
            found[example_id] = example
    return found


@dataclass(frozen=True)
class RunRequest:
    transcript: str
    source_name: str
    meeting_date: date | None
    vendor: str
    effort: str
    mode: str
    example: Example | None


def parse_run_request(payload: object, examples: dict[str, Example]) -> RunRequest:
    if not isinstance(payload, dict):
        raise RequestError("request body must be a JSON object")
    transcript = payload.get("transcript")
    if not isinstance(transcript, str) or not transcript.strip():
        raise RequestError("transcript is required")
    if len(transcript.encode("utf-8")) > MAX_TRANSCRIPT_BYTES:
        raise RequestError(f"transcript is larger than {MAX_TRANSCRIPT_BYTES // 1024} kB")
    if not parse_transcript(transcript).turns:
        raise RequestError("no speaker turns found; expected lines like '**Name:** text' or 'Name: text'")

    mode = payload.get("mode", "live")
    if mode not in MODES:
        raise RequestError(f"mode must be one of: {', '.join(MODES)}")
    example = None
    if mode == "example":
        example_id = payload.get("example_id")
        if not isinstance(example_id, str) or example_id not in examples:
            raise RequestError(f"unknown example_id: {example_id!r}")
        example = examples[example_id]
        # The saved extraction only matches its own transcript; quotes would not verify against edits.
        expected = example.transcript_path.read_text(encoding="utf-8-sig")
        if _normalize_newlines(transcript).strip() != expected.strip():
            raise RequestError(
                "example mode needs the unchanged example transcript; use live analysis for edited text"
            )
        transcript = expected

    effort = payload.get("effort", llm.DEFAULT_EFFORT)
    if effort not in EFFORTS:
        raise RequestError(f"effort must be one of: {', '.join(EFFORTS)}")
    return RunRequest(
        transcript=transcript,
        source_name=_text_field(payload, "source_name", "rozmowa.md", MAX_SOURCE_NAME),
        meeting_date=_parse_meeting_date(payload.get("meeting_date")),
        vendor=_text_field(payload, "vendor", "Rinvo", MAX_VENDOR),
        effort=effort,
        mode=mode,
        example=example,
    )


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _text_field(payload: dict[str, Any], name: str, default: str, max_length: int) -> str:
    value = payload.get(name)
    if value is None:
        return default
    if not isinstance(value, str) or len(value) > max_length:
        raise RequestError(f"{name} must be a string of at most {max_length} characters")
    return value.strip() or default


def _parse_meeting_date(value: object) -> date | None:
    if value is None or value == "":
        return None
    # fromisoformat alone would also accept forms like '20261006'.
    if not isinstance(value, str) or not _ISO_DATE_RE.fullmatch(value):
        raise RequestError("meeting_date must be YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise RequestError(f"meeting_date is not a valid date: {value}") from exc


@dataclass
class Run:
    id: str
    mode: str
    source_name: str
    created_at: float
    status: str = "queued"
    started_at: float | None = None
    finished_at: float | None = None
    error: str | None = None
    warnings: list[str] = field(default_factory=list)
    summary: dict[str, Any] | None = None

    def to_json(self) -> dict[str, Any]:
        elapsed = None
        if self.started_at is not None:
            elapsed = round((self.finished_at or time.time()) - self.started_at, 1)
        files = None
        if self.status == "done":
            files = {
                "report_html": f"/runs/{self.id}/{HTML_REPORT_FILE}",
                "report_md": f"/runs/{self.id}/{REPORT_FILE}",
                "outbox": f"/runs/{self.id}/{OUTBOX_FILE}",
            }
        return {
            "id": self.id,
            "status": self.status,
            "mode": self.mode,
            "source_name": self.source_name,
            "created_at": _iso(self.created_at),
            "started_at": _iso(self.started_at),
            "finished_at": _iso(self.finished_at),
            "elapsed_s": elapsed,
            "error": self.error,
            "warnings": list(self.warnings),
            "summary": self.summary,
            "files": files,
        }

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Run:
        return cls(
            id=data["id"],
            mode=data["mode"],
            source_name=data["source_name"],
            created_at=_timestamp(data["created_at"]) or 0.0,
            status=data["status"],
            started_at=_timestamp(data.get("started_at")),
            finished_at=_timestamp(data.get("finished_at")),
            error=data.get("error"),
            warnings=list(data.get("warnings") or []),
            summary=data.get("summary"),
        )


def _iso(timestamp: float | None) -> str | None:
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp).astimezone().isoformat(timespec="milliseconds")


def _timestamp(value: str | None) -> float | None:
    return datetime.fromisoformat(value).timestamp() if value else None


@dataclass
class PipelineResult:
    summary: dict[str, Any]
    result: dict[str, Any]


class RunManager:
    """Keeps runs in memory, mirrors them to runs/<id>/run.json and executes them one at a time."""

    def __init__(self, root: Path, examples: dict[str, Example] | None = None):
        self.root = root.resolve()
        self.examples = find_examples() if examples is None else examples
        self._runs: dict[str, Run] = {}
        self._lock = threading.Lock()
        self._queue: queue.Queue[tuple[Run, RunRequest] | None] = queue.Queue()
        self._load_existing()
        self._worker = threading.Thread(target=self._work, name="callflow-runs", daemon=True)
        self._worker.start()

    def close(self) -> None:
        self._queue.put(None)
        self._worker.join(timeout=5)

    def submit(self, request: RunRequest) -> Run:
        now = time.time()
        with self._lock:
            if request.mode == "live" and any(
                run.mode == "live" and run.status in ("queued", "running") for run in self._runs.values()
            ):
                # Live runs call the paid model; a double submit must not start a second one.
                raise BusyError("a live analysis is already queued or running; wait for it to finish")
            run_id = self._new_id(now)
            run = Run(run_id, request.mode, request.source_name, created_at=now)
            self._runs[run_id] = run
        run_dir = self.run_dir(run_id)
        try:
            run_dir.mkdir(parents=True)
            (run_dir / TRANSCRIPT_FILE).write_text(request.transcript, encoding="utf-8", newline="")
            self._save(run)
        except OSError:
            with self._lock:
                del self._runs[run_id]
            raise
        self._queue.put((run, request))
        return run

    def get(self, run_id: str) -> dict[str, Any] | None:
        with self._lock:
            run = self._runs.get(run_id)
            return run.to_json() if run else None

    def list(self) -> list[dict[str, Any]]:
        with self._lock:
            runs = sorted(self._runs.values(), key=lambda run: (run.created_at, run.id), reverse=True)
            return [run.to_json() for run in runs]

    def result(self, run_id: str) -> dict[str, Any] | None:
        """The result of a finished run; None if it is not done (callers check existence with get)."""
        with self._lock:
            run = self._runs.get(run_id)
            if run is None or run.status != "done":
                return None
        try:
            return json.loads((self.run_dir(run_id) / RESULT_FILE).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ResultFileError(f"cannot read the result of run {run_id}: {exc}") from exc

    def run_dir(self, run_id: str) -> Path:
        return self.root / run_id

    def _new_id(self, now: float) -> str:
        stamp = datetime.fromtimestamp(now).strftime("%Y%m%d-%H%M%S")
        while True:
            run_id = f"{stamp}-{secrets.token_hex(2)}"
            if run_id not in self._runs and not self.run_dir(run_id).exists():
                return run_id

    def _load_existing(self) -> None:
        if not self.root.is_dir():
            return
        for path in self.root.glob(f"*/{RUN_FILE}"):
            try:
                run = Run.from_json(json.loads(path.read_text(encoding="utf-8")))
            except (OSError, ValueError, KeyError, TypeError) as exc:
                log.warning("skipping unreadable run %s: %s", path, exc)
                continue
            if run.status in ("queued", "running"):
                run.status = "error"
                run.error = "interrupted: the server stopped before the run finished"
                run.finished_at = run.finished_at or run.started_at or run.created_at
            self._runs[run.id] = run

    def _save(self, run: Run) -> None:
        with self._lock:
            data = run.to_json()
        write_json(self.run_dir(run.id) / RUN_FILE, data)

    def _work(self) -> None:
        while (job := self._queue.get()) is not None:
            try:
                self._execute(*job)
            except Exception:  # a dead worker would leave every later run queued forever
                log.exception("run %s: unexpected failure in the worker", job[0].id)

    def _execute(self, run: Run, request: RunRequest) -> None:
        with self._lock:
            run.status = "running"
            run.started_at = time.time()
        status, error, summary = "error", None, None
        try:
            self._save(run)
            outcome = run_pipeline(request, self.run_dir(run.id), run.warnings)
            write_json(self.run_dir(run.id) / RESULT_FILE, outcome.result)
            status, summary = "done", outcome.summary
        except (llm.LLMError, ExtractionError, ValueError, OSError) as exc:
            error = str(exc)
        except Exception as exc:  # keep the worker alive for the next run; details go to the log
            log.exception("run %s failed unexpectedly", run.id)
            error = f"internal error: {exc!r}"
        with self._lock:
            run.status, run.error, run.summary = status, error, summary
            run.finished_at = time.time()
        try:
            self._save(run)
        except OSError:
            log.exception("could not save the state of run %s", run.id)


def run_pipeline(request: RunRequest, out_dir: Path, warnings: list[str]) -> PipelineResult:
    """Mirror of cli.run for one web request; warnings are appended as they are found."""
    transcript = parse_transcript(request.transcript, source=request.source_name)
    if not transcript.turns:
        raise ValueError("no speaker turns found in the transcript")
    out_dir.mkdir(parents=True, exist_ok=True)
    cost_usd = duration_s = None
    if request.example is not None:
        extraction = load_extraction(request.example.extraction_path)
        write_json(out_dir / EXTRACTION_FILE, extraction.model_dump(mode="json"))
        if request.meeting_date and request.meeting_date != extraction.meeting_date:
            warnings.append(
                f"example mode uses the saved extraction; meeting date {request.meeting_date} was ignored"
            )
    else:
        meeting_date = _meeting_date(request, transcript, warnings)
        extraction, raw = _extract_and_save(request, meeting_date, out_dir)
        cost_usd = _number(raw.get("total_cost_usd"))
        duration_ms = _number(raw.get("duration_ms"))
        duration_s = round(duration_ms / 1000, 1) if duration_ms is not None else None

    report = verify(extraction, transcript)
    routed = route(extraction)
    write_outputs(routed, report, out_dir, request.source_name)
    html = render_html(routed, report, request.source_name)
    (out_dir / HTML_REPORT_FILE).write_text(html, encoding="utf-8")
    return PipelineResult(
        summary=_summary(extraction, report, cost_usd, duration_s),
        result=_result(extraction, report, build_outbox(routed, report)),
    )


def _meeting_date(request: RunRequest, transcript: Transcript, warnings: list[str]) -> date | None:
    if request.meeting_date:
        return request.meeting_date
    if transcript.call_date:
        return date.fromisoformat(transcript.call_date)
    warnings.append(
        "meeting date not found in the transcript; relative deadlines will not be resolved "
        "(set the meeting date to fix)"
    )
    return None


def _extract_and_save(
    request: RunRequest, meeting_date: date | None, out_dir: Path
) -> tuple[MeetingExtraction, dict[str, Any]]:
    try:
        extraction, raw = extract(request.transcript, meeting_date, request.vendor, effort=request.effort)
    except ExtractionError as exc:
        if exc.raw is not None:
            write_json(out_dir / RAW_RESPONSE_FILE, exc.raw)
        raise
    write_json(out_dir / RAW_RESPONSE_FILE, raw)
    write_json(out_dir / EXTRACTION_FILE, extraction.model_dump(mode="json"))
    return extraction, raw


def _number(value: object) -> float | None:
    return float(value) if isinstance(value, int | float) and not isinstance(value, bool) else None


def _summary(
    extraction: MeetingExtraction,
    report: VerificationReport,
    cost_usd: float | None,
    duration_s: float | None,
) -> dict[str, Any]:
    return {
        "client": extraction.client,
        "meeting_date": extraction.meeting_date.isoformat() if extraction.meeting_date else None,
        "items": len(extraction.items),
        "guardrails": len(extraction.guardrails),
        "drafts": len(extraction.drafts),
        "quotes_verified": sum(check.verified for check in report.quotes),
        "quotes_total": len(report.quotes),
        "issues": len(report.issues),
        "cost_usd": cost_usd,
        "duration_s": duration_s,
    }


def _result(
    extraction: MeetingExtraction, report: VerificationReport, outbox: dict[str, Any]
) -> dict[str, Any]:
    quotes: dict[str, list[dict[str, Any]]] = {}
    for check in report.quotes:
        quotes.setdefault(check.owner_id, []).append(
            {"speaker": check.speaker, "quote": check.quote, "line": check.line, "verified": check.verified}
        )
    return {
        "outbox": outbox,
        "quotes": quotes,
        "summary_text": extraction.summary,
        "participants": extraction.participants,
        "assumptions": extraction.assumptions,
    }
