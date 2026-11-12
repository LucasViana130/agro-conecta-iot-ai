import json
import socket
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener, HTTPRedirectHandler


class ApiError(RuntimeError):
    def __init__(self, message, status=None):
        super().__init__(message)
        self.status = status


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward bearer tokens to another origin.


class JavaClient:
    def __init__(self, config):
        self.config = config
        self._token = config.token
        self._opener = build_opener(NoRedirect)

    def request(self, method, path, body=None):
        if not path.startswith("/api/") or "://" in path:
            raise ValueError("Rota interna inválida")
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self._token:
            headers["Authorization"] = "Bearer " + self._token
        attempts = 3 if method == "GET" else 1
        for attempt in range(attempts):
            req = Request(self.config.base_url + path,
                          data=None if body is None else json.dumps(body, allow_nan=False).encode(),
                          headers=headers, method=method)
            try:
                with self._opener.open(req, timeout=self.config.timeout) as response:
                    return json.loads(response.read())
            except HTTPError as error:
                status = error.code
                error.close()
                if status not in (429, 502, 503, 504) or attempt == attempts - 1:
                    raise ApiError(f"API retornou HTTP {status}; detalhes omitidos", status) from None
            except (URLError, TimeoutError, socket.timeout, ConnectionError):
                if attempt == attempts - 1:
                    raise ApiError("Falha de conexão/timeout; detalhes omitidos") from None
            except (ValueError, UnicodeError):
                raise ApiError("Resposta JSON inválida; conteúdo omitido") from None
            time.sleep(.1 * (2 ** attempt))
        raise ApiError("Tentativas esgotadas")

    def login(self):
        if not self._token:
            if not self.config.username or not self.config.password:
                raise ApiError("Configure token ou usuário e senha por variáveis de ambiente")
            response = self.request("POST", "/api/auth/login",
                                    {"email": self.config.username, "password": self.config.password})
            self._token = response.get("token")
            if not isinstance(self._token, str) or not self._token:
                raise ApiError("Resposta de autenticação inválida")

    def send(self, reading):
        reading.validate()
        response = self.request("POST", "/api/simulated-readings", reading.payload())
        if response.get("source") != "SIMULATED":
            raise ApiError("Java não preservou origem SIMULATED")
        return response

    def analyze(self, crop_id):
        job = self.request("POST", f"/api/crop-areas/{crop_id}/risk-jobs")
        for _ in range(30):
            job = self.request("GET", f"/api/risk-jobs/{job['id']}")
            if job.get("status") in ("COMPLETED", "COMPLETED_WITHOUT_AI"):
                return job
            if job.get("status") == "FAILED":
                raise ApiError("Job de análise falhou")
            time.sleep(1)
        raise ApiError("Análise não concluiu dentro de 30 consultas")
