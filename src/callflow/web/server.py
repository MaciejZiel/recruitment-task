"""Local HTTP server for the callflow web interface (standard library only)."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import socket
import sys
import traceback
from collections.abc import Callable
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

from callflow.web.runs import (
    RUN_ID_PATTERN,
    BusyError,
    RequestError,
    ResultFileError,
    RunManager,
    parse_run_request,
)

STATIC_DIR = Path(__file__).resolve().parent / "static"
INDEX_FILE = "index.html"
# Bound before reading: the transcript limit is 300 kB, JSON escaping can at most ~6x it.
MAX_BODY_BYTES = 2 * 1024 * 1024

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    # text/plain so browsers display the markdown instead of downloading it.
    ".md": "text/plain; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".ico": "image/x-icon",
    ".woff2": "font/woff2",
}

RUN_RE = re.compile(rf"/api/runs/(?P<id>{RUN_ID_PATTERN})")
RESULT_RE = re.compile(rf"/api/runs/(?P<id>{RUN_ID_PATTERN})/result")
RUN_FILE_RE = re.compile(rf"/runs/(?P<id>{RUN_ID_PATTERN})/(?P<path>.+)")


class CallflowServer(ThreadingHTTPServer):
    daemon_threads = True
    # On Windows SO_REUSEADDR lets a second server bind a port that is already in use.
    allow_reuse_address = sys.platform != "win32"

    def __init__(
        self,
        address: tuple[str, int],
        manager: RunManager,
        static_dir: Path = STATIC_DIR,
        allow_remote: bool = False,
    ):
        if ":" in address[0]:
            self.address_family = socket.AF_INET6
        super().__init__(address, Handler)
        self.manager = manager
        self.static_dir = static_dir
        self.allow_remote = allow_remote


class Handler(BaseHTTPRequestHandler):
    server: CallflowServer
    server_version = "callflow-web"
    # Socket timeout: a client that stops sending must not hold a thread forever.
    timeout = 30

    def do_GET(self) -> None:
        self._dispatch(self._handle_get)

    def do_POST(self) -> None:
        self._dispatch(self._handle_post)

    def _dispatch(self, handle: Callable[[], None]) -> None:
        try:
            handle()
        except ConnectionError:  # the client went away; there is nobody to answer
            self.close_connection = True
        except Exception:
            self.log_error("unhandled error for %s %s\n%s", self.command, self.path, traceback.format_exc())
            # A response may already be partly written; never reuse this connection.
            self.close_connection = True
            try:
                self._send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "internal server error")
            except OSError:
                return

    def _handle_get(self) -> None:
        if not self._host_allowed():
            return
        path = unquote(urlsplit(self.path).path)
        manager = self.server.manager
        if path == "/":
            self._send_file(self.server.static_dir, INDEX_FILE)
        elif path.startswith("/static/"):
            self._send_file(self.server.static_dir, path.removeprefix("/static/"))
        elif path == "/api/examples":
            self._send_json([example.to_json() for example in manager.examples.values()])
        elif path == "/api/runs":
            self._send_json(manager.list())
        elif match := RUN_RE.fullmatch(path):
            run = manager.get(match["id"])
            if run is None:
                self._send_error(HTTPStatus.NOT_FOUND, "unknown run")
            else:
                self._send_json(run)
        elif match := RESULT_RE.fullmatch(path):
            self._send_result(match["id"])
        elif match := RUN_FILE_RE.fullmatch(path):
            if manager.get(match["id"]) is None:
                self._send_error(HTTPStatus.NOT_FOUND, "unknown run")
            else:
                self._send_file(manager.run_dir(match["id"]), match["path"])
        else:
            self._send_error(HTTPStatus.NOT_FOUND, "not found")

    def _handle_post(self) -> None:
        if not self._host_allowed():
            return
        if urlsplit(self.path).path != "/api/runs":
            self._send_error(HTTPStatus.NOT_FOUND, "not found")
            return
        if not self._same_origin():
            self._send_error(HTTPStatus.FORBIDDEN, "cross-origin requests are not allowed")
            return
        try:
            payload = self._read_json()
            request = parse_run_request(payload, self.server.manager.examples)
        except RequestError as exc:
            self._send_error(HTTPStatus.BAD_REQUEST, str(exc))
            return
        try:
            run = self.server.manager.submit(request)
        except BusyError as exc:
            self._send_error(HTTPStatus.CONFLICT, str(exc))
            return
        except OSError as exc:
            self._send_error(HTTPStatus.INTERNAL_SERVER_ERROR, f"could not create the run: {exc}")
            return
        self._send_json({"id": run.id}, HTTPStatus.ACCEPTED)

    def _read_json(self) -> Any:
        try:
            length = int(self.headers.get("Content-Length", ""))
        except ValueError:
            raise RequestError("Content-Length header is required") from None
        if length < 0:
            self.close_connection = True  # rfile.read(-1) would wait for the client to close
            raise RequestError("Content-Length must not be negative")
        if length > MAX_BODY_BYTES:
            self.close_connection = True  # the unread body would otherwise be parsed as the next request
            raise RequestError("request body is too large")
        body = self.rfile.read(length)
        try:
            return json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RequestError(f"invalid JSON: {exc}") from None
        except RecursionError:
            raise RequestError("invalid JSON: nesting is too deep") from None

    def _send_result(self, run_id: str) -> None:
        manager = self.server.manager
        run = manager.get(run_id)
        if run is None:
            self._send_error(HTTPStatus.NOT_FOUND, "unknown run")
            return
        try:
            result = manager.result(run_id)
        except ResultFileError as exc:
            self.log_error("%s", exc)
            self._send_error(
                HTTPStatus.INTERNAL_SERVER_ERROR, "the result file of this run is missing or unreadable"
            )
            return
        if result is None:
            self._send_error(HTTPStatus.CONFLICT, f"run is {run['status']}, the result is not available")
        else:
            self._send_json(result)

    def _host_allowed(self) -> bool:
        """Without --allow-remote only loopback Host names are served (blocks DNS rebinding)."""
        if self.server.allow_remote:
            return True
        hostname = urlsplit("//" + self.headers.get("Host", "")).hostname
        if hostname and is_loopback(hostname):
            return True
        self._send_error(HTTPStatus.FORBIDDEN, "host not allowed")
        return False

    def _same_origin(self) -> bool:
        """Browsers send Origin with cross-site POSTs; a live run costs money, so refuse them."""
        origin = self.headers.get("Origin")
        return origin is None or urlsplit(origin).netloc == self.headers.get("Host")

    def _send_file(self, base: Path, relative: str) -> None:
        path = safe_path(base, relative)
        if path is None:
            self._send_error(HTTPStatus.NOT_FOUND, "not found")
            return
        try:
            body = path.read_bytes()
        except OSError:
            self._send_error(HTTPStatus.NOT_FOUND, "not found")
            return
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", CONTENT_TYPES.get(path.suffix.lower(), "application/octet-stream"))
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, data: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, status: HTTPStatus, message: str) -> None:
        self._send_json({"error": message}, status)

    def log_request(self, code: int | str = "-", size: int | str = "-") -> None:
        # The frontend polls run status every second; log only writes and failures.
        if self.command != "GET" or not isinstance(code, int) or code >= 400:
            super().log_request(code, size)


def safe_path(base: Path, relative: str) -> Path | None:
    """The file `relative` inside `base`, or None if it is missing or escapes `base`."""
    # ':' would reach drive letters and NTFS alternate data streams (report.md::$DATA) on Windows.
    if not relative or any(char in relative for char in "\\\x00:") or ".." in relative.split("/"):
        return None
    try:
        root = base.resolve()
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            return None
    except (OSError, ValueError):
        return None
    return path


def is_loopback(host: str) -> bool:
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="callflow-web", description="Local web interface for callflow.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument(
        "--allow-remote",
        action="store_true",
        help="allow a non-loopback --host; the server has no authentication",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    # Windows consoles and pipes default to a legacy code page; log lines may contain Polish text.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = build_parser()
    args = parser.parse_args(argv)
    if not is_loopback(args.host) and not args.allow_remote:
        parser.error(
            f"--host {args.host} is not a loopback address; the server has no authentication, "
            "pass --allow-remote to expose it anyway"
        )

    manager = RunManager(Path.cwd() / "runs")
    try:
        server = CallflowServer((args.host, args.port), manager, allow_remote=args.allow_remote)
    except OSError as exc:
        manager.close()
        parser.exit(1, f"callflow-web: cannot listen on {args.host}:{args.port}: {exc}\n")
    host, port = server.server_address[:2]
    shown_host = f"[{host}]" if ":" in str(host) else host
    print(
        f"callflow web: http://{shown_host}:{port}/  (runs stored in {manager.root}; Ctrl+C to stop)",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        manager.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
