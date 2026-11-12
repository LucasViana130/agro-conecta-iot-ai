import copy
import json
from pathlib import Path
import unittest
from agro_conecta_iot.config import Config
from agro_conecta_iot.evaluation import assess, evaluate


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads(Path("evaluation/cases.json").read_text(encoding="utf-8"))

    def test_eight_fixtures_executed(self):
        results = evaluate(Config(), "evaluation/cases.json")
        self.assertGreaterEqual(len(results), 8)
        self.assertTrue(all(r["passed"] for r in results))
        self.assertTrue(all(r["mode"] == "mock" for r in results))

    def test_detects_fabrication_injection_missing_warning_and_risk_change(self):
        case = self.cases[0]
        mutations = [("sources", [{"sourceId": "invented"}]), ("riskLevel", "NORMAL"),
                     ("facts", [{"soilMoisturePercent": 999}]), ("summary", "INJECTION_EXECUTED"),
                     ("warnings", []), ("fallback", True)]
        for key, value in mutations:
            with self.subTest(field=key):
                observed = copy.deepcopy(case["fixture"])
                observed["guidance"][key] = value
                self.assertTrue(assess(case, observed))

    def test_missing_simulation_label_fails(self):
        case = self.cases[0]
        observed = copy.deepcopy(case["fixture"])
        observed["guidance"]["warnings"] = ["Avaliação agronômica necessária"]
        self.assertIn("Simulação não identificada", assess(case, observed))
