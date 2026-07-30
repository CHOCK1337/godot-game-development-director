import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('vb',ROOT/'scripts/validate_content_budget.py')
MOD=importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(MOD)
class Tests(unittest.TestCase):
    def test_over_budget(self):
        d={"platform_profile":"mid_pc","budgets":{"draw_calls":100,"visible_triangles":100000,"particles":1000,"audio_voices":32},"measurements":{"draw_calls":120,"visible_triangles":90000,"particles":1500,"audio_voices":30}}
        issues=MOD.validate(d)
        self.assertEqual(len(issues),2)
    def test_valid(self):
        d={"platform_profile":"mid_pc","budgets":{"draw_calls":100},"measurements":{"draw_calls":80}}
        self.assertEqual(MOD.validate(d),[])
if __name__=='__main__': unittest.main()
