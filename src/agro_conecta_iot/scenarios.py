"""Only inputs; Java calculates indicators and risk."""
from datetime import datetime, timezone, timedelta
import random
from .models import Reading, utc

SCENARIOS = ("normal", "attention", "critical", "insufficient-data", "sensor-stale", "possible-sensor-fault")


def generate(scenario, seed=2026, sensor_id=1, reference=None):
    if scenario not in SCENARIOS:
        raise ValueError("Cenário desconhecido")
    now = utc(reference or datetime.now(timezone.utc)).replace(microsecond=0)
    rng = random.Random(seed)
    rows = []
    for index in range(6):
        temperature, humidity, soil = {
            "normal": (25, 65, 28), "attention": (29 + index * .3, 55 - index, 21 - index * .4),
            "critical": (32 + index * .5, 40 - index, 19 - index),
            "insufficient-data": (25, 65, None), "sensor-stale": (25, 65, 28),
            "possible-sensor-fault": (25, 65, 28),
        }[scenario]
        if scenario != "possible-sensor-fault":
            temperature = round(temperature + rng.uniform(-.05, .05), 3)
            humidity = round(humidity + rng.uniform(-.05, .05), 3)
            if soil is not None:
                soil = round(soil + rng.uniform(-.01, .01), 3)
        at = now - timedelta(minutes=10 * (5 - index))
        if scenario == "sensor-stale":
            at -= timedelta(hours=25)
        rows.append(Reading(sensor_id, at.isoformat().replace("+00:00", "Z"), temperature, humidity, soil).validate(now))
    return rows
