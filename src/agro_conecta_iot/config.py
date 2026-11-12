from dataclasses import dataclass, field
import os
from urllib.parse import urlsplit


@dataclass(frozen=True)
class Config:
    base_url: str = "http://localhost:8080"
    username: str = field(default="", repr=False)
    password: str = field(default="", repr=False)
    token: str = field(default="", repr=False)
    timeout: float = 10
    seed: int = 2026
    crop_id: int = 1
    sensor_id: int = 1

    def __post_init__(self):
        url = urlsplit(self.base_url)
        if url.scheme not in ("http", "https") or not url.hostname or url.username or url.password or url.query or url.fragment:
            raise ValueError("URL inválida; não inclua credenciais")
        if url.scheme == "http" and url.hostname not in ("localhost", "127.0.0.1", "host.docker.internal", "::1"):
            raise ValueError("Use HTTPS fora do ambiente local")
        if not 0 < self.timeout <= 120 or self.crop_id < 1 or self.sensor_id < 1:
            raise ValueError("Timeout ou IDs inválidos")

    @classmethod
    def from_env(cls):
        return cls(os.getenv("JAVA_API_BASE_URL", "http://localhost:8080").rstrip("/"),
                   os.getenv("JAVA_API_USERNAME", ""), os.getenv("JAVA_API_PASSWORD", ""),
                   os.getenv("JAVA_API_TOKEN", ""), float(os.getenv("HTTP_TIMEOUT_SECONDS", "10")),
                   int(os.getenv("SIMULATOR_SEED", "2026")), int(os.getenv("CROP_AREA_ID") or "1"),
                   int(os.getenv("SENSOR_ID") or "1"))
