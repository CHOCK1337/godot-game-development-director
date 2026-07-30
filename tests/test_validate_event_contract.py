import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('events',ROOT/'scripts/validate_event_contract.py')
MOD=importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(MOD)
class Tests(unittest.TestCase):
    def test_example_valid(self):
        data=json.loads((ROOT/'examples/11-event-contract.json').read_text(encoding='utf-8'))
        self.assertEqual(MOD.validate(data)['errors'],[])
    def test_duplicate_fails(self):
        data=json.loads((ROOT/'examples/11-event-contract.json').read_text(encoding='utf-8'))
        data['events'].append(dict(data['events'][0]))
        self.assertTrue(any('duplicate' in e for e in MOD.validate(data)['errors']))
if __name__=='__main__': unittest.main()
