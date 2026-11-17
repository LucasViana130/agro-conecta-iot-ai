"""Basic local/CI guard, not a replacement for GitHub secret scanning."""
import json
import argparse
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser(description="Verifica segredos, JSON e prontidão opcional da entrega.")
parser.add_argument("--delivery", action="store_true", help="Falha também em pendências humanas/evidências finais.")
args = parser.parse_args()

files = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard"], text=True).splitlines()
patterns = [re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"), re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
            re.compile(r"AQ\.[A-Za-z0-9_-]{30,}"),
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

if args.delivery:
    delivery_errors = []
    identification = Path("entrega/identificacao.txt").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    evidence = Path("docs/evidencias/README.md").read_text(encoding="utf-8")

    if "[PREENCHER]" in identification or "# Repita a linha" in identification:
        delivery_errors.append("Preencher nomes, RMs e turmas em entrega/identificacao.txt e remover instruções.")
    if "PENDENTE DE DADOS DO GRUPO" in readme:
        delivery_errors.append("Identificar os integrantes também no README.")
    if "precisa ser reexecutada" in evidence:
        delivery_errors.append("Reexecutar a integração contra o commit Java final e atualizar as evidências.")

    required = [
        "docs/evidencias/evaluation-mock.json",
        "docs/evidencias/gemini-live.json",
        "docs/evidencias/java-integration.json",
        "knowledge-base/sources.json",
        "docs/arquitetura.md",
        "docs/avaliacao-ia.md",
        "docs/seguranca-e-limitacoes.md",
    ]
    missing = [name for name in required if not Path(name).is_file()]
    if missing:
        delivery_errors.append("Arquivos obrigatórios ausentes: " + ", ".join(missing))

    if delivery_errors:
        raise SystemExit("Preflight de entrega pendente:\n- " + "\n- ".join(delivery_errors))
    print("Preflight de entrega: identificação e evidências finais conferidas")
