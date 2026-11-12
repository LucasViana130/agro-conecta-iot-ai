"""Run from repository root after pip install -e ."""
from agro_conecta_iot.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["evaluate"]))
