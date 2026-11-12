import argparse
import json
import os
from pathlib import Path
from .config import Config
from .models import utc
from .scenarios import SCENARIOS
from .simulator import simulate
from .evaluation import evaluate
from .java_client import ApiError


def main(argv=None):
    parser = argparse.ArgumentParser(description="Agro Conecta IoT/IA")
    commands = parser.add_subparsers(dest="command", required=True)
    sim = commands.add_parser("simulate")
    sim.add_argument("--scenario", choices=SCENARIOS, default="normal")
    sim.add_argument("--dry-run", action="store_true")
    sim.add_argument("--reference", help="Instante ISO 8601; fixe junto da seed para reprodução exata")
    evaluation = commands.add_parser("evaluate")
    evaluation.add_argument("--live", action="store_true")
    evaluation.add_argument("--cases", default="evaluation/cases.json")
    evaluation.add_argument("--bindings", help="JSON local caso -> jobId e retrievedSourceIds independentes")
    evaluation.add_argument("--output", default="reports/evaluation.json")
    args = parser.parse_args(argv)
    try:
        config = Config.from_env()
        if args.command == "simulate":
            result = simulate(config, args.scenario, args.dry_run, utc(args.reference) if args.reference else None)
        else:
            mode = os.getenv("EVALUATION_MODE", "mock")
            if mode not in ("mock", "live"):
                raise ValueError("EVALUATION_MODE deve ser mock ou live")
            result = evaluate(config, args.cases, args.live or mode == "live", args.bindings)
            destination = Path(args.output)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if isinstance(result, list) and any(not r["passed"] for r in result) else 0
    except (ApiError, ValueError, OSError, KeyError, TypeError):
        print(json.dumps({"error": "Falha de configuração, validação ou integração; detalhes omitidos por segurança."}))
        return 1
