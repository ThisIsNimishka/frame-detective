"""
app/server.py
-------------
Minimal HTTP server. Routes every request to the correct view renderer.
No external dependencies — stdlib only.
"""
import socket
import threading
import time
import webbrowser
import http.server
import socketserver
from typing import Callable

from app.views import ROUTES


class _Handler(http.server.BaseHTTPRequestHandler):
    """Request handler — looks up path in ROUTES, calls renderer, returns HTML."""

    routes: dict[str, Callable[[], str]] = {}   # filled by Server before listen

    def do_GET(self):
        path = self.path.split("?")[0]           # strip query strings
        renderer = self.routes.get(path)

        if renderer:
            try:
                html  = renderer()
                data  = html.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type",   "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control",  "no-cache, no-store, must-revalidate")
                self.end_headers()
                self.wfile.write(data)
            except Exception as exc:
                self._error(500, f"<pre>Render error: {exc}</pre>")
        else:
            self._error(404, f"<p>No route for <code>{path}</code></p>")

    def _error(self, code: int, body: str):
        msg  = f"<html><body><h2>{code}</h2>{body}</body></html>"
        data = msg.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type",   "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        # Replace default log with a cleaner one-liner
        print(f"  [{self.command}] {self.path}")


class Server:
    """
    Wraps TCPServer. Resolves a free port, injects routes, then:
      - starts the server in a daemon thread
      - opens the browser
      - blocks on KeyboardInterrupt
    """

    def __init__(self, port: int = 0):
        self.port = port or self._free_port()

    @staticmethod
    def _free_port() -> int:
        with socket.socket() as s:
            s.bind(("", 0))
            return s.getsockname()[1]

    def run(self):
        url = f"http://127.0.0.1:{self.port}"

        # Inject routes into handler class
        _Handler.routes = ROUTES

        httpd = socketserver.TCPServer(("127.0.0.1", self.port), _Handler)
        httpd.allow_reuse_address = True

        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()

        self._print_banner(url)
        time.sleep(0.4)
        webbrowser.open(url)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n  Shutting down. Goodbye, Detective!")
            httpd.shutdown()

    @staticmethod
    def _print_banner(url: str):
        print()
        print("  ╔══════════════════════════════════════════════════╗")
        print("  ║      FRAME DETECTIVE — PresentMon Learning       ║")
        print("  ╠══════════════════════════════════════════════════╣")
        print(f"  ║  Server : {url:<38} ║")
        print("  ║  Open   : your browser launched automatically   ║")
        print("  ║  Quit   : Ctrl+C                                ║")
        print("  ╚══════════════════════════════════════════════════╝")
        print()
