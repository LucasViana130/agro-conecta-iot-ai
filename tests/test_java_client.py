import json
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from agro_conecta_iot.config import Config
from agro_conecta_iot.java_client import JavaClient, ApiError
from agro_conecta_iot.scenarios import generate


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def handle_request(self):
        self.server.calls += 1
        length = int(self.headers.get("Content-Length", 0))
        self.server.body = json.loads(self.rfile.read(length)) if length else None
        if self.server.delay:
            time.sleep(self.server.delay)
        status = self.server.status
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        body = self.server.body or {"ok": True}
        if status != 200:
            body = {"error": "TOP_SECRET_TOKEN"}
        try:
            self.wfile.write(json.dumps(body).encode())
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass

    do_GET = handle_request
    do_POST = handle_request


class HttpTests(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.calls, self.server.status, self.server.delay = 0, 200, 0
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.client = JavaClient(Config(base_url=f"http://127.0.0.1:{self.server.server_port}",
                                        token="TOP_SECRET_TOKEN", timeout=.1))

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def test_real_http_payload(self):
        row = generate("critical")[0]
        self.assertEqual("SIMULATED", self.client.send(row)["source"])
        self.assertEqual(row.payload(), self.server.body)

    def test_get_retries_are_bounded(self):
        self.server.status = 503
        with self.assertRaises(ApiError) as error:
            self.client.request("GET", "/api/test")
        self.assertEqual(3, self.server.calls)
        self.assertNotIn("TOP_SECRET_TOKEN", str(error.exception))

    def test_bad_request_not_retried(self):
        self.server.status = 400
        with self.assertRaises(ApiError):
            self.client.request("GET", "/api/test")
        self.assertEqual(1, self.server.calls)

    def test_write_timeout_is_not_replayed(self):
        self.server.delay = .3
        with self.assertRaises(ApiError):
            self.client.request("POST", "/api/test", {"x": 1})
        self.assertEqual(1, self.server.calls)

    def test_get_timeout_is_bounded(self):
        self.server.delay = .3
        with self.assertRaises(ApiError):
            self.client.request("GET", "/api/test")
        self.assertEqual(3, self.server.calls)
