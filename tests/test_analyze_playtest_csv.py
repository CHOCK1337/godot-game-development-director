import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('playtest',ROOT/'scripts/analyze_playtest_csv.py')
MOD=importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(MOD)
class Tests(unittest.TestCase):
    def test_summary(self):
        result=MOD.analyze(ROOT/'examples/09-playtest-events.csv')
        self.assertEqual(result['sessions'],2)
        self.assertEqual(result['completion_rate'],1.0)
        self.assertEqual(result['failures'],2)
        self.assertGreater(result['music_state_changes_per_minute'],0)
if __name__=='__main__': unittest.main()
