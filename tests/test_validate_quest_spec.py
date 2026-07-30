import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('vq',ROOT/'scripts/validate_quest_spec.py')
MOD=importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(MOD)
class Tests(unittest.TestCase):
    def test_valid_graph(self):
        data={"quest_id":"q1","start_node":"start","nodes":[{"id":"start","type":"objective"},{"id":"end","type":"terminal"}],"edges":[{"from":"start","to":"end","condition":"always"}],"fail_states":["abandon"],"save_keys":["quest.q1.state"]}
        self.assertEqual(MOD.validate(data),[])
    def test_unreachable_and_no_terminal(self):
        data={"quest_id":"q","start_node":"a","nodes":[{"id":"a","type":"objective"},{"id":"b","type":"objective"}],"edges":[],"fail_states":[],"save_keys":[]}
        issues=MOD.validate(data)
        self.assertTrue(any("unreachable" in x.lower() for x in issues))
        self.assertTrue(any("terminal" in x.lower() for x in issues))
if __name__=='__main__': unittest.main()
