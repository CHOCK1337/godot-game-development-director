import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('gameplay',ROOT/'scripts/validate_gameplay_spec.py')
MOD=importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(MOD)
class Tests(unittest.TestCase):
    def test_example_valid(self):
        data=json.loads((ROOT/'examples/10-gameplay-spec.json').read_text(encoding='utf-8'))
        self.assertEqual(MOD.validate(data)['errors'],[])
    def test_missing_cost_fails(self):
        data=json.loads((ROOT/'examples/10-gameplay-spec.json').read_text(encoding='utf-8'))
        del data['mechanics'][0]['cost']
        self.assertTrue(any('cost' in e for e in MOD.validate(data)['errors']))
if __name__=='__main__': unittest.main()
