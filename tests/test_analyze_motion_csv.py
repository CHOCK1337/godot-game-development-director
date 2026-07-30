import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).parents[1] / "scripts" / "analyze_motion_csv.py"
spec = importlib.util.spec_from_file_location("motion_analyzer", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class MotionAnalyzerTests(unittest.TestCase):
    def test_flags_sliding_contact_foot(self):
        csv_text = """time,root_x,root_y,root_z,left_x,left_y,left_z,right_x,right_y,right_z,left_contact,right_contact
0.0,0,1,0,0,0,0,0,0,0,1,0
0.1,0,1,0.1,0,0,0.02,0,0.1,0.1,1,0
0.2,0,1,0.2,0,0,0.04,0,0,0.2,1,1
0.3,0,1,0.3,0,0.1,0.1,0,0,0.22,0,1
"""
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "capture.csv"
            path.write_text(csv_text, encoding="utf-8")
            report = module.analyze(module.load_rows(path), 0.04)
        self.assertTrue(any("left" in flag for flag in report["flags"]))
        self.assertGreater(report["feet"]["left"]["p95_contact_speed"], 0.04)

    def test_rejects_missing_columns(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "bad.csv"
            path.write_text("time,root_x\n0,0\n1,1\n2,2\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                module.load_rows(path)


if __name__ == "__main__":
    unittest.main()
