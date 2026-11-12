import unittest
from dataclasses import replace
from datetime import datetime, timezone, timedelta
from agro_conecta_iot.models import Reading
from agro_conecta_iot.scenarios import generate, SCENARIOS
from agro_conecta_iot.simulator import simulate
from agro_conecta_iot.config import Config


class Scenarios(unittest.TestCase):
    now = datetime(2026, 11, 11, tzinfo=timezone.utc)

    def test_seed_and_timestamp_reproduce_every_scenario(self):
        for scenario in SCENARIOS:
            with self.subTest(scenario=scenario):
                rows = generate(scenario, reference=self.now)
                self.assertEqual(rows, generate(scenario, reference=self.now))
                self.assertEqual(6, len(rows))
                self.assertTrue(all(r.source == "SIMULATED" for r in rows))
                for row in rows:
                    row.validate(self.now)

    def test_missing_data_and_fault_are_explicit(self):
        self.assertTrue(all(r.soilMoisturePercent is None for r in generate("insufficient-data", reference=self.now)))
        self.assertEqual(1, len({r.soilMoisturePercent for r in generate("possible-sensor-fault", reference=self.now)}))

    def test_validation_rejects_invalid_values_without_clamping(self):
        row = Reading(1, self.now.isoformat(), 25, 65, 28)
        for name, value in [("soilMoisturePercent", -1), ("airHumidityPercent", 101), ("batteryPercent", 101),
                            ("temperatureCelsius", float("nan")), ("rainfallMillimeters", -1),
                            ("source", "MANUAL"), ("sensorId", 0),
                            ("measuredAt", (self.now + timedelta(minutes=6)).isoformat()),
                            ("measuredAt", "2026-11-11T00:00:00")]:
            with self.subTest(field=name):
                with self.assertRaises(ValueError):
                    replace(row, **{name: value}).validate(self.now)

    def test_dry_run_has_no_authentication_dependency(self):
        result = simulate(Config(), "critical", True, self.now)
        self.assertEqual("dry-run", result["mode"])
        self.assertEqual("SIMULATED", result["readings"][0]["source"])
