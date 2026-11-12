"""Basic local/CI guard, not a replacement for GitHub secret scanning."""
import json
from pathlib import Path
import re
import subprocess

files = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard"], text=True).splitlines()
patterns = [re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"), re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
            re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
            re.compile(r"eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}")]
errors = []
for name in files:
    path = Path(name)
    if path.name.startswith(".env") and path.name != ".env.example":
        errors.append("Arquivo de ambiente indevido")
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeError, IsADirectoryError):
        continue
    if any(p.search(text) for p in patterns):
        errors.append(f"Possível segredo em {name}")
    if path.suffix == ".json":
        json.loads(text)
if errors:
    raise SystemExit("\n".join(errors))
print(f"JSON e verificação básica de segredos: {len(files)} arquivos verificados")
