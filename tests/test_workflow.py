import json
import tempfile
import unittest
from pathlib import Path
from repair_agent.runner import DEMO, repair_demo


class WorkflowTests(unittest.TestCase):
    def test_finds_patch_without_changing_original(self):
        original = (DEMO / "calculator.py").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "artifacts"
            report = repair_demo(out)
            self.assertFalse(report["baseline_passed"])
            self.assertTrue(report["repair_found"])
            self.assertIn("+", (out / "proposed_fix.patch").read_text())
            self.assertTrue(json.loads((out / "report.json").read_text())["repair_found"])
        self.assertEqual(original, (DEMO / "calculator.py").read_text())


if __name__ == "__main__":
    unittest.main()
