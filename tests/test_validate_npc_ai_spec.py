import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('vn',ROOT/'scripts/validate_npc_ai_spec.py')
MOD=importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(MOD)
class Tests(unittest.TestCase):
    def test_valid(self):
        d={"agent_id":"guard","initial_state":"idle","states":["idle","investigate","combat"],"transitions":[{"from":"idle","to":"investigate","trigger":"heard_noise"},{"from":"investigate","to":"combat","trigger":"confirmed_target"},{"from":"combat","to":"idle","trigger":"lost_target_timeout"}],"perception":{"sight":True,"hearing":True},"fallback_state":"idle","debug_fields":["state","target","last_stimulus"]}
        self.assertEqual(MOD.validate(d),[])
    def test_missing_recovery(self):
        d={"agent_id":"x","initial_state":"combat","states":["combat"],"transitions":[],"perception":{},"fallback_state":"missing","debug_fields":[]}
        issues=MOD.validate(d)
        self.assertTrue(any("fallback" in x.lower() for x in issues))
        self.assertTrue(any("debug" in x.lower() for x in issues))
if __name__=='__main__': unittest.main()
