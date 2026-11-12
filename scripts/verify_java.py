"""Opt-in integration against a real local Java API with disposable test data.
Creates two producers, a farm and one isolated crop/sensor per scenario. Never prints tokens.
Run only against a development database. APP_DEMO_ENABLED=true is required.
"""
from dataclasses import replace
from datetime import datetime, timezone, timedelta
from pathlib import Path
import json
import secrets
from agro_conecta_iot.config import Config
from agro_conecta_iot.java_client import JavaClient, ApiError
from agro_conecta_iot.scenarios import SCENARIOS, generate


def run():
    config = Config.from_env()
    client = JavaClient(replace(config, token="", username="", password=""))
    suffix = secrets.token_hex(6)
    auth = client.request("POST", "/api/auth/register", {
        "name": "Produtor teste IoT", "email": f"iot-{suffix}@example.test", "password": secrets.token_urlsafe(24)})
    client._token = auth["token"]
    other = JavaClient(replace(config, token=""))
    other._token = other.request("POST", "/api/auth/register", {
        "name": "Outro produtor", "email": f"other-{suffix}@example.test",
        "password": secrets.token_urlsafe(24)})["token"]
    farm = client.request("POST", "/api/farms", {
        "name": "Fazenda simulada", "city": "Campinas", "state": "SP", "totalArea": 10, "areaUnit": "HECTARE"})
    results = []
    expected = {"normal": "NORMAL", "attention": "ATTENTION", "critical": "CRITICAL",
                "insufficient-data": "INSUFFICIENT_DATA", "sensor-stale": "INSUFFICIENT_DATA",
                "possible-sensor-fault": "NORMAL"}
    for scenario in SCENARIOS:
        crop = client.request("POST", "/api/crop-areas", {
            "farmId": farm["id"], "name": f"DEMO {scenario}", "cropType": "Milho",
            "areaSize": 1, "areaUnit": "HECTARE"})
        client.request("PUT", f"/api/crop-areas/{crop['id']}/agronomic-profile", {
            "soilTexture": "DEMO", "fieldCapacityPercent": 32, "wiltingPointPercent": 12,
            "rootDepthCentimeters": 30, "sensorDepthCentimeters": 15, "source": "DEMO - não calibrado em campo", "demo": True})
        sensor = client.request("POST", "/api/sensors", {
            "cropAreaId": crop["id"], "name": f"DEMO {scenario}", "deviceCode": f"{suffix}-{scenario}",
            "sensorType": "WEATHER_STATION"})
        rows = generate(scenario, sensor_id=sensor["id"])
        for row in rows:
            response = client.send(row)
            assert response["source"] == "SIMULATED"
        job = client.analyze(crop["id"])
        assert job["result"]["riskLevel"] == expected[scenario], (scenario, job["result"])
        health = client.request("GET", f"/api/sensors/{sensor['id']}/health")
        if scenario == "possible-sensor-fault":
            assert health["calculatedHealth"] == "POSSIBLE_FAULT"
        if scenario == "sensor-stale":
            assert health["calculatedHealth"] == "STALE"
        guidance = client.request("POST", f"/api/risk-jobs/{job['id']}/guidance")
        assert guidance["result"] == job["result"]
        assert guidance["guidance"]["fallback"] is True  # This verification runs with AI disabled.
        assert guidance["guidance"]["sources"] == []
        assert "simulad" in json.dumps(guidance["guidance"]).lower()
        for path in (f"/api/risk-jobs/{job['id']}/guidance", "/api/simulated-readings"):
            try:
                other.request("POST", path, rows[0].payload() if path.endswith("readings") else None)
                raise AssertionError("Cross-owner access allowed")
            except ApiError as error:
                assert error.status == 404
        for bad in (replace(rows[0], soilMoisturePercent=101),
                    replace(rows[0], measuredAt=(datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat())):
            try:
                client.request("POST", "/api/simulated-readings", bad.payload())
                raise AssertionError("Invalid reading accepted")
            except ApiError as error:
                assert error.status == 400
        try:
            JavaClient(replace(config, token="")).request("POST", "/api/simulated-readings", rows[0].payload())
            raise AssertionError("Anonymous reading accepted")
        except ApiError as error:
            assert error.status == 401
        results.append({"scenario": scenario, "riskLevel": job["result"]["riskLevel"],
                        "calculatedHealth": health["calculatedHealth"], "guidanceFallback": True,
                        "simulatedSource": True, "ownerIsolation": True, "invalidInputRejected": True,
                        "anonymousRejected": True, "passed": True})
    report = {"executedAt": datetime.now(timezone.utc).isoformat(), "mode": "real-java-local-ai-disabled",
              "scenarios": results, "limitations": ["Gemini não foi chamado", "Banco de desenvolvimento; dados descartáveis"]}
    destination = Path("reports/java-integration.json")
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run()
