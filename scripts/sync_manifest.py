"""Generate manifest from Java's actual corpus; does not copy full publications."""
import argparse
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("java_repo", type=Path)
args = parser.parse_args()
sources = []
for file in sorted((args.java_repo / "src/main/resources/rag/agronomy").glob("*.md")):
    raw = file.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
    header, _ = raw.decode("utf-8").replace("\r\n", "\n").split("\n---\n", 1)
    metadata = dict(line.split(": ", 1) for line in header.splitlines() if ": " in line)
    sources.append({**metadata, "section": metadata["title"], "cultureOrTheme": metadata["topic"],
                    "javaPath": str(file.relative_to(args.java_repo)).replace("\\", "/"),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "hashScope": "UTF-8/LF do resumo controlado no Java; não do documento remoto",
                    "usage": "Resumo didático autoral; publicação original não redistribuída. Verificar termos da fonte.",
                    "verification": "URL conferida em 2026-11-11" if metadata["sourceId"] in
                        ("embrapa-umidade-familiar", "fao-irrigation-management") else
                        "Revalidação remota bloqueada (403/timeout); revisar manualmente antes da entrega"})
Path("knowledge-base/sources.json").write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(sources)} fontes e hashes extraídos do Java")
