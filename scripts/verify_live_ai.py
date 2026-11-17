"""Valida uma orientacao real do Java sem exportar credenciais ou o texto gerado.

Cria dados DEMO descartaveis no ambiente configurado e exige IA habilitada.
As credenciais aleatorias ficam apenas em memoria.
"""

from dataclasses import replace
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import secrets

from agro_conecta_iot.config import Config
from agro_conecta_iot.java_client import JavaClient
from agro_conecta_iot.scenarios import generate


def run():
    config = replace(Config.from_env(), token="", username="", password="")
    client = JavaClient(config)
    suffix = secrets.token_hex(6)
    auth = client.request(
        "POST",
        "/api/auth/register",
        {
            "name": "Produtor DEMO IA",
            "email": f"demo-ia-{suffix}@example.test",
            "password": secrets.token_urlsafe(24),
        },
    )
    client._token = auth["token"]

    farm = client.request(
        "POST",
        "/api/farms",
        {"name": "Fazenda DEMO IA", "city": "Campinas", "state": "SP", "totalArea": 1, "areaUnit": "HECTARE"},
    )
    crop = client.request(
        "POST",
        "/api/crop-areas",
        {"farmId": farm["id"], "name": "Milho DEMO IA", "cropType": "Milho", "areaSize": 1, "areaUnit": "HECTARE"},
    )
    client.request(
        "PUT",
        f"/api/crop-areas/{crop['id']}/agronomic-profile",
        {
            "soilTexture": "DEMO",
            "fieldCapacityPercent": 32,
            "wiltingPointPercent": 12,
            "rootDepthCentimeters": 30,
            "sensorDepthCentimeters": 15,
            "source": "DEMO - nao calibrado em campo",
            "demo": True,
        },
    )
    sensor = client.request(
        "POST",
        "/api/sensors",
        {
            "cropAreaId": crop["id"],
            "name": "Estacao DEMO IA",
            "deviceCode": f"demo-ia-{suffix}",
            "sensorType": "WEATHER_STATION",
        },
    )
    for reading in generate("critical", sensor_id=sensor["id"]):
        client.send(reading)

    job = client.analyze(crop["id"])
    risk_before = job["result"]["riskLevel"]
    response = client.request("POST", f"/api/risk-jobs/{job['id']}/guidance")
    guidance = response["guidance"]
    sources = guidance.get("sources", [])
    risk_after = response["result"]["riskLevel"]

    if guidance.get("fallback") is not False:
        raise RuntimeError(f"IA real indisponivel; fallback={guidance.get('reason', 'SEM_MOTIVO')}")
    if risk_before != risk_after or guidance.get("riskLevel") != risk_before:
        raise RuntimeError("A orientacao alterou ou contradisse o risco deterministico")
    if not sources:
        raise RuntimeError("A orientacao real nao retornou fontes recuperadas")

    stored = client.request("POST", f"/api/risk-jobs/{job['id']}/guidance")["guidance"]
    if stored.get("generatedAt") != guidance.get("generatedAt"):
        raise RuntimeError("A orientacao nao foi reutilizada de forma idempotente")

    allowed_source_fields = ("sourceId", "title", "institution", "url", "version")
    report = {
        "executedAt": datetime.now(timezone.utc).isoformat(),
        "mode": "real-java-render-ai-enabled",
        "javaCommit": os.getenv("JAVA_COMMIT", "nao-informado"),
        "scenario": "critical",
        "riskBefore": risk_before,
        "riskAfter": risk_after,
        "riskPreserved": True,
        "fallback": False,
        "model": guidance.get("model"),
        "promptVersion": guidance.get("promptVersion"),
        "sourceCount": len(sources),
        "sources": [{field: source.get(field) for field in allowed_source_fields} for source in sources],
        "warningCount": len(guidance.get("warnings", [])),
        "storedIdempotently": True,
        "contentStoredInEvidence": False,
        "limitations": [
            "Dados e perfil agronomico demonstrativos",
            "Resposta integral omitida da evidencia; revisao humana continua obrigatoria",
        ],
    }
    destination = Path("reports/gemini-live.json")
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run()
