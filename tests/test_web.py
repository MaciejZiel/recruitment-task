import http.client
import json
import socket
import threading
import time
from datetime import date
from pathlib import Path

import pytest

from callflow.extract import ExtractionError
from callflow.llm import LLMError
from callflow.schema import MeetingExtraction
from callflow.web import runs, server
from callflow.web.runs import RunManager
from callflow.web.server import CallflowServer

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
AUTO_TAMA_TRANSCRIPT = (EXAMPLES / "transkrypcja-spotkanie.md").read_text(encoding="utf-8-sig")
AUTO_TAMA_EXTRACTION = EXAMPLES / "output" / "auto-tama" / "extraction.json"
AUTO_TAMA_OUTBOX = EXAMPLES / "output" / "auto-tama" / "outbox.json"
UNKNOWN_RUN = "20260101-000000-abcd"


class Client:
    def __init__(self, port: int):
        self.port = port

    def request(self, method: str, path: str, body: object = None, headers: dict | None = None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        data = body if isinstance(body, bytes) or body is None else json.dumps(body).encode("utf-8")
        connection.request(method, path, body=data, headers=headers or {})
        response = connection.getresponse()
        payload = response.read()
        connection.close()
        return response.status, response.getheader("Content-Type"), payload

    def json(self, method: str, path: str, body: object = None, headers: dict | None = None):
        status, _, payload = self.request(method, path, body, headers)
        return status, json.loads(payload)

    def wait(self, run_id: str, timeout: float = 30) -> dict:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            status, run = self.json("GET", f"/api/runs/{run_id}")
            assert status == 200
            if run["status"] in ("done", "error"):
                return run
            time.sleep(0.05)
        raise AssertionError(f"run {run_id} did not finish: {run}")


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    static = tmp_path / "static"
    static.mkdir()
    (static / "index.html").write_text("<!doctype html><title>callflow</title>", encoding="utf-8")
    (static / "app.css").write_text("body{}", encoding="utf-8")
    (static / "app.js").write_text("console.log(1)", encoding="utf-8")
    manager = RunManager(Path("runs"))
    httpd = CallflowServer(("127.0.0.1", 0), manager, static_dir=static)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield Client(httpd.server_address[1])
    httpd.shutdown()
    httpd.server_close()
    manager.close()


def example_request(**overrides) -> dict:
    return {"transcript": AUTO_TAMA_TRANSCRIPT, "mode": "example", "example_id": "auto-tama"} | overrides


def live_request(**overrides) -> dict:
    return {"transcript": AUTO_TAMA_TRANSCRIPT, "source_name": "spotkanie.md", "mode": "live"} | overrides


def fake_extract(calls: list | None = None, release: threading.Event | None = None):
    def extract(transcript_text, meeting_date, vendor, *, model=None, effort=None):
        if calls is not None:
            calls.append({"meeting_date": meeting_date, "vendor": vendor, "effort": effort})
        if release is not None:
            release.wait(10)
        extraction = MeetingExtraction.model_validate_json(AUTO_TAMA_EXTRACTION.read_text(encoding="utf-8"))
        return extraction, {"total_cost_usd": 0.5, "duration_ms": 61234, "structured_output": {}}

    return extract


def test_index_and_static_files(client):
    status, content_type, body = client.request("GET", "/")
    assert status == 200 and content_type.startswith("text/html") and b"callflow" in body
    assert client.request("GET", "/static/app.css")[1].startswith("text/css")
    assert client.request("GET", "/static/app.js")[1].startswith("text/javascript")
    assert client.request("GET", "/static/missing.js")[0] == 404


def test_examples_list_auto_tama_with_transcript(client):
    status, examples = client.json("GET", "/api/examples")
    assert status == 200
    by_id = {example["id"]: example for example in examples}
    assert {"auto-tama", "dentavita"} <= set(by_id)
    auto_tama = by_id["auto-tama"]
    assert auto_tama["title"].startswith("Grupa Auto Tama × Rinvo")
    assert auto_tama["transcript_name"] == "transkrypcja-spotkanie.md"
    assert auto_tama["transcript"] == AUTO_TAMA_TRANSCRIPT


def test_example_run_completes_with_auto_tama_numbers(client, tmp_path):
    status, created = client.json("POST", "/api/runs", example_request())
    assert status == 202
    run = client.wait(created["id"])

    assert run["status"] == "done", run["error"]
    assert run["mode"] == "example" and run["error"] is None
    assert run["summary"] == {
        "client": "Grupa Auto Tama",
        "meeting_date": "2026-10-06",
        "items": 37,
        "guardrails": 11,
        "drafts": 8,
        "quotes_verified": 108,
        "quotes_total": 108,
        # The committed demo is regenerated with the current verify(), so its warnings are the reference.
        "issues": len(json.loads(AUTO_TAMA_OUTBOX.read_text(encoding="utf-8"))["issues"]),
        "cost_usd": None,
        "duration_s": None,
    }
    assert run["source_name"] == "rozmowa.md"
    assert run["elapsed_s"] is not None and run["finished_at"] is not None
    run_dir = tmp_path / "runs" / run["id"]
    assert (run_dir / "transcript.md").read_text(encoding="utf-8") == AUTO_TAMA_TRANSCRIPT
    assert len(list((run_dir / "drafts").glob("D*.md"))) == 8

    for key, content_type in [
        ("report_html", "text/html"),
        ("report_md", "text/plain"),
        ("outbox", "application/json"),
    ]:
        status, served_type, _ = client.request("GET", run["files"][key])
        assert status == 200 and served_type.startswith(content_type)
    draft = next((run_dir / "drafts").glob("D01-*.md")).name
    assert client.request("GET", f"/runs/{run['id']}/drafts/{draft}")[0] == 200

    status, listed = client.json("GET", "/api/runs")
    assert status == 200 and [entry["id"] for entry in listed] == [run["id"]]


def test_result_returns_outbox_and_quotes(client, tmp_path):
    run_id = client.json("POST", "/api/runs", example_request())[1]["id"]
    client.wait(run_id)

    status, result = client.json("GET", f"/api/runs/{run_id}/result")

    assert status == 200
    outbox_file = tmp_path / "runs" / run_id / "outbox.json"
    assert result["outbox"] == json.loads(outbox_file.read_text(encoding="utf-8"))
    assert result["quotes"]["A01"][0].keys() == {"speaker", "quote", "line", "verified"}
    assert sum(len(quotes) for quotes in result["quotes"].values()) == 108
    assert "G01" in result["quotes"]
    assert result["summary_text"] and result["participants"] and isinstance(result["assumptions"], list)


def test_live_run_uses_parsed_date_and_records_cost(client, tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(runs, "extract", fake_extract(calls))

    run_id = client.json("POST", "/api/runs", live_request(effort="low", vendor="Acme"))[1]["id"]
    run = client.wait(run_id)

    assert run["status"] == "done", run["error"]
    assert calls == [{"meeting_date": date(2026, 10, 6), "vendor": "Acme", "effort": "low"}]
    assert run["summary"]["cost_usd"] == 0.5 and run["summary"]["duration_s"] == 61.2
    assert run["source_name"] == "spotkanie.md" and run["warnings"] == []
    run_dir = tmp_path / "runs" / run_id
    assert (run_dir / "raw_response.json").is_file() and (run_dir / "extraction.json").is_file()


def test_live_run_meeting_date_from_request_overrides_header(client, monkeypatch):
    calls = []
    monkeypatch.setattr(runs, "extract", fake_extract(calls))
    run_id = client.json("POST", "/api/runs", live_request(meeting_date="2026-10-07"))[1]["id"]
    client.wait(run_id)
    assert calls[0]["meeting_date"] == date(2026, 10, 7)


def test_live_run_without_date_warns(client, monkeypatch):
    calls = []
    monkeypatch.setattr(runs, "extract", fake_extract(calls))
    transcript = "**Anna:** Filtr nie działa.\n**Marek:** Sprawdzę.\n"
    run = client.wait(client.json("POST", "/api/runs", live_request(transcript=transcript))[1]["id"])
    assert calls[0]["meeting_date"] is None
    assert any("meeting date" in warning for warning in run["warnings"])


def test_result_is_409_until_the_run_is_done(client, monkeypatch):
    release = threading.Event()
    monkeypatch.setattr(runs, "extract", fake_extract(release=release))
    run_id = client.json("POST", "/api/runs", live_request())[1]["id"]

    status, body = client.json("GET", f"/api/runs/{run_id}/result")
    assert status == 409 and "error" in body
    assert client.json("GET", f"/api/runs/{run_id}")[1]["files"] is None

    release.set()
    assert client.wait(run_id)["status"] == "done"
    assert client.json("GET", f"/api/runs/{run_id}/result")[0] == 200


@pytest.mark.parametrize(
    ("error", "expected"),
    [
        (ExtractionError("model output does not match the schema", raw={"is_error": False}), "schema"),
        (LLMError("claude -p failed"), "claude -p failed"),
    ],
)
def test_live_run_failure_is_reported_and_server_keeps_working(
    client, tmp_path, monkeypatch, error, expected
):
    def failing_extract(*args, **kwargs):
        raise error

    monkeypatch.setattr(runs, "extract", failing_extract)
    run = client.wait(client.json("POST", "/api/runs", live_request())[1]["id"])

    assert run["status"] == "error" and expected in run["error"]
    assert run["summary"] is None and run["files"] is None
    raw_saved = (tmp_path / "runs" / run["id"] / "raw_response.json").is_file()
    assert raw_saved == isinstance(error, ExtractionError)
    assert client.wait(client.json("POST", "/api/runs", example_request())[1]["id"])["status"] == "done"


@pytest.mark.parametrize(
    ("body", "message"),
    [
        (b"{not json", "invalid JSON"),
        ([], "JSON object"),
        ({"transcript": "   ", "mode": "live"}, "transcript is required"),
        ({"transcript": "**A:** " + "x" * 300 * 1024, "mode": "live"}, "larger than"),
        ({"transcript": "Brak dialogu w tym pliku.", "mode": "live"}, "no speaker turns"),
        (live_request(meeting_date="06.10.2026"), "YYYY-MM-DD"),
        (live_request(meeting_date="2026-02-30"), "not a valid date"),
        (live_request(effort="max"), "effort"),
        (live_request(mode="batch"), "mode"),
        (example_request(example_id="nope"), "unknown example_id"),
        (example_request(example_id=None), "unknown example_id"),
        (live_request(vendor=5), "vendor"),
    ],
)
def test_invalid_run_requests_are_rejected(client, body, message):
    status, payload = client.json("POST", "/api/runs", body, {"Content-Type": "application/json"})
    assert status == 400
    assert message in payload["error"]
    assert client.json("GET", "/api/runs")[1] == []


@pytest.mark.parametrize(
    "path",
    [
        f"/api/runs/{UNKNOWN_RUN}",
        f"/api/runs/{UNKNOWN_RUN}/result",
        f"/runs/{UNKNOWN_RUN}/report.html",
        "/api/runs/not-a-run",
        "/api/nothing",
    ],
)
def test_unknown_paths_are_404(client, path):
    status, payload = client.json("GET", path)
    assert status == 404 and "error" in payload


def test_path_traversal_is_blocked(client):
    run_id = client.json("POST", "/api/runs", example_request())[1]["id"]
    client.wait(run_id)
    paths = [
        "/static/../server.py",
        "/static/%2e%2e/server.py",
        "/static/..%5cserver.py",
        "/static/../../../../pyproject.toml",
        f"/static/../runs/{run_id}/report.md",
        f"/runs/{run_id}/../../static/index.html",
        f"/runs/{run_id}/../../pyproject.toml",
        f"/runs/{run_id}/..%2f..%2fpyproject.toml",
        f"/runs/{run_id}/drafts/../../../pyproject.toml",
        f"/runs/{run_id}/C:/Windows/win.ini",
        f"/runs/{run_id}/drafts",
        "/static/app.js%00",
        f"/runs/{run_id}/report.md%00.html",
        f"/runs/{run_id}/report.md::$DATA",
        # UNC and absolute paths: on Windows `root / "//host/share/x"` would open an SMB connection.
        "/static//127.0.0.1/share/x",
        f"/runs/{run_id}//127.0.0.1/share/x",
        f"/runs/{run_id}/%2f%2f127.0.0.1/share/x",
        f"/runs/{run_id}/%2fpyproject.toml",
        f"/runs/{run_id}/drafts//D01.md",
        f"/runs/{run_id}/./report.md",
        f"/runs/{run_id}/drafts/./D01.md",
        f"/runs/{run_id}/report.md/",
        f"/runs/{run_id}/%5c%5c127.0.0.1%5cshare%5cx",
    ]
    for path in paths:
        status, _, payload = client.request("GET", path)
        assert status in (400, 404), path
        assert "error" in json.loads(payload), path


def test_safe_path_rejects_unc_and_dot_segments_before_touching_the_filesystem(tmp_path, monkeypatch):
    def no_filesystem(*args, **kwargs):
        raise AssertionError("safe_path touched the filesystem")

    monkeypatch.setattr(Path, "resolve", no_filesystem)
    for relative in [
        "//host/share/x",
        "/etc/passwd",
        "a//b",
        "./a",
        "a/.",
        "a/../b",
        "a/",
        "\\\\host\\share",
        "",
    ]:
        assert server.safe_path(tmp_path, relative) is None, relative


def test_responses_forbid_framing(client):
    for path in ("/", "/api/runs"):
        connection = http.client.HTTPConnection("127.0.0.1", client.port, timeout=10)
        connection.request("GET", path)
        response = connection.getresponse()
        response.read()
        connection.close()
        assert response.status == 200, path
        assert response.getheader("X-Frame-Options") == "DENY", path
        assert response.getheader("Content-Security-Policy") == "frame-ancestors 'none'", path


def test_foreign_host_and_cross_origin_post_are_refused(client):
    assert client.request("GET", "/api/runs", headers={"Host": "evil.example:8000"})[0] == 403
    host = f"127.0.0.1:{client.port}"
    status, _ = client.json(
        "POST", "/api/runs", example_request(), {"Host": host, "Origin": "http://evil.example"}
    )
    assert status == 403
    status, _ = client.json(
        "POST", "/api/runs", example_request(), {"Host": host, "Origin": f"http://{host}"}
    )
    assert status == 202


def test_runs_survive_a_restart(tmp_path):
    root = tmp_path / "runs"
    manager = RunManager(root)
    done_id = manager.submit(runs.parse_run_request(example_request(), manager.examples)).id
    deadline = time.monotonic() + 30
    while manager.get(done_id)["status"] != "done" and time.monotonic() < deadline:
        time.sleep(0.05)
    manager.close()
    interrupted = root / "20260101-000000-0000"
    interrupted.mkdir()
    (interrupted / "run.json").write_text(
        json.dumps(
            {
                "id": interrupted.name,
                "mode": "live",
                "source_name": "a.md",
                "status": "running",
                "created_at": "2026-01-01T00:00:00+01:00",
                "started_at": "2026-01-01T00:00:01+01:00",
            }
        ),
        encoding="utf-8",
    )

    restarted = RunManager(root)
    try:
        listed = {run["id"]: run for run in restarted.list()}
        assert listed[done_id]["status"] == "done" and listed[done_id]["summary"]["items"] == 37
        assert restarted.result(done_id)["outbox"]["client"] == "Grupa Auto Tama"
        assert listed[interrupted.name]["status"] == "error"
        assert "interrupted" in listed[interrupted.name]["error"]
    finally:
        restarted.close()


@pytest.mark.parametrize("host", ["0.0.0.0", "192.168.1.10", "example.com"])
def test_non_loopback_host_is_refused_without_allow_remote(host, capsys):
    with pytest.raises(SystemExit) as exc:
        server.main(["--host", host])
    assert exc.value.code == 2
    assert "--allow-remote" in capsys.readouterr().err


def test_loopback_detection():
    assert server.is_loopback("127.0.0.1") and server.is_loopback("::1") and server.is_loopback("localhost")
    assert server.is_loopback("127.0.0.2")
    assert not server.is_loopback("0.0.0.0")


def test_any_loopback_host_header_is_served(client):
    assert client.request("GET", "/api/runs", headers={"Host": f"127.0.0.2:{client.port}"})[0] == 200


def raw_request(port: int, request: bytes) -> bytes:
    with socket.create_connection(("127.0.0.1", port), timeout=5) as sock:
        sock.sendall(request)
        chunks = []
        while chunk := sock.recv(65536):
            chunks.append(chunk)
    return b"".join(chunks)


def test_negative_content_length_is_rejected_without_reading(client):
    response = raw_request(
        client.port,
        f"POST /api/runs HTTP/1.1\r\nHost: 127.0.0.1:{client.port}\r\nContent-Length: -1\r\n\r\n".encode(),
    )
    assert response.startswith(b"HTTP/1.0 400") or response.startswith(b"HTTP/1.1 400")
    assert b"negative" in response
    assert client.json("GET", "/api/runs")[1] == []


def test_deeply_nested_json_is_rejected(client):
    status, payload = client.json("POST", "/api/runs", b"[" * 100_000)
    assert status == 400 and "invalid JSON" in payload["error"]
    assert client.json("GET", "/api/runs")[1] == []


def test_worker_survives_a_failed_run(client, monkeypatch):
    original_save = RunManager._save
    failed = []

    def save(self, run):
        if run.status == "running" and not failed:
            failed.append(run.id)
            raise OSError("disk full")
        original_save(self, run)

    monkeypatch.setattr(RunManager, "_save", save)
    run = client.wait(client.json("POST", "/api/runs", example_request())[1]["id"])
    assert run["status"] == "error" and "disk full" in run["error"] and run["finished_at"] is not None
    assert client.wait(client.json("POST", "/api/runs", example_request())[1]["id"])["status"] == "done"


def test_worker_survives_an_unexpected_exception(client, monkeypatch):
    original_pipeline = runs.run_pipeline
    calls = []

    def pipeline_failing_once(*args, **kwargs):
        calls.append(1)
        if len(calls) == 1:
            raise RuntimeError("boom")
        return original_pipeline(*args, **kwargs)

    monkeypatch.setattr(runs, "run_pipeline", pipeline_failing_once)
    run = client.wait(client.json("POST", "/api/runs", example_request())[1]["id"])
    assert run["status"] == "error" and "boom" in run["error"]
    assert client.wait(client.json("POST", "/api/runs", example_request())[1]["id"])["status"] == "done"


def test_only_one_live_run_at_a_time(client, monkeypatch):
    release = threading.Event()
    monkeypatch.setattr(runs, "extract", fake_extract(release=release))
    status, first = client.json("POST", "/api/runs", live_request())
    assert status == 202

    status, body = client.json("POST", "/api/runs", live_request())
    assert status == 409 and "already" in body["error"]
    status, example = client.json("POST", "/api/runs", example_request())
    assert status == 202

    release.set()
    assert client.wait(first["id"])["status"] == "done"
    assert client.wait(example["id"])["status"] == "done"
    status, again = client.json("POST", "/api/runs", live_request())
    assert status == 202
    assert client.wait(again["id"])["status"] == "done"


def test_example_mode_refuses_an_edited_transcript(client):
    edited = AUTO_TAMA_TRANSCRIPT + "\n**Anna:** Jeszcze jedna sprawa.\n"
    status, payload = client.json("POST", "/api/runs", example_request(transcript=edited))
    assert status == 400 and "live analysis" in payload["error"]
    assert client.json("GET", "/api/runs")[1] == []


def test_example_mode_accepts_crlf_line_endings(client, tmp_path):
    crlf = AUTO_TAMA_TRANSCRIPT.replace("\n", "\r\n")
    status, created = client.json("POST", "/api/runs", example_request(transcript=crlf))
    assert status == 202
    run = client.wait(created["id"])
    assert run["status"] == "done" and run["summary"]["quotes_verified"] == 108
    saved = (tmp_path / "runs" / run["id"] / "transcript.md").read_bytes().decode("utf-8")
    assert saved == AUTO_TAMA_TRANSCRIPT


def test_missing_result_file_is_500(client, tmp_path):
    run_id = client.json("POST", "/api/runs", example_request())[1]["id"]
    assert client.wait(run_id)["status"] == "done"
    (tmp_path / "runs" / run_id / "result.json").unlink()

    status, payload = client.json("GET", f"/api/runs/{run_id}/result")
    assert status == 500 and "error" in payload


def test_unexpected_handler_error_is_500(client, monkeypatch):
    def broken_list(self):
        raise RuntimeError("boom")

    monkeypatch.setattr(RunManager, "list", broken_list)
    status, payload = client.json("GET", "/api/runs")
    assert status == 500 and payload == {"error": "internal server error"}


def test_port_in_use_is_refused(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    manager = RunManager(tmp_path / "runs")
    first = CallflowServer(("127.0.0.1", 0), manager)
    port = first.server_address[1]
    try:
        with pytest.raises(OSError):
            CallflowServer(("127.0.0.1", port), manager)
        with pytest.raises(SystemExit) as exc:
            server.main(["--port", str(port)])
        assert exc.value.code == 1
        assert "cannot listen" in capsys.readouterr().err
    finally:
        first.server_close()
        manager.close()
