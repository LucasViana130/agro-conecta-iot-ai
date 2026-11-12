from .java_client import JavaClient
from .scenarios import generate


def simulate(config, scenario, dry_run=False, reference=None):
    rows = generate(scenario, config.seed, config.sensor_id, reference)
    if dry_run:
        return {"mode": "dry-run", "scenario": scenario, "seed": config.seed,
                "cropAreaId": config.crop_id, "readings": [row.payload() for row in rows]}
    client = JavaClient(config)
    client.login()
    sensor = client.request("GET", f"/api/sensors/{config.sensor_id}")
    if sensor.get("cropAreaId") != config.crop_id or sensor.get("sensorType") != "WEATHER_STATION":
        raise ValueError("Use WEATHER_STATION pertencente ao cultivo configurado")
    sent = [client.send(row) for row in rows]
    job = client.analyze(config.crop_id)
    health = client.request("GET", f"/api/sensors/{config.sensor_id}/health")
    return {"mode": "java", "scenario": scenario, "readingIds": [row["id"] for row in sent],
            "jobId": job["id"], "result": job["result"], "health": health}
