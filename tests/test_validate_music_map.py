import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('music',ROOT/'scripts/validate_music_map.py')
MOD=importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(MOD)
class Tests(unittest.TestCase):
    def test_example_valid(self):
        data=json.loads((ROOT/'examples/08-music-state-map.json').read_text(encoding='utf-8'))
        self.assertEqual(MOD.validate(data)['errors'],[])
    def test_unknown_state_fails(self):
        data=json.loads((ROOT/'examples/08-music-state-map.json').read_text(encoding='utf-8'))
        data['transitions'][0]['to']='missing'
        self.assertTrue(any('unknown to state' in e for e in MOD.validate(data)['errors']))
    def test_unreachable_state_warns(self):
        data=json.loads((ROOT/'examples/08-music-state-map.json').read_text(encoding='utf-8'))
        data['states'].append({'id':'orphan','purpose':'test','bpm':96,'meter':'4/4','min_hold_seconds':1,'layers':['x']})
        self.assertTrue(any('unreachable' in w for w in MOD.validate(data)['warnings']))
if __name__=='__main__': unittest.main()
