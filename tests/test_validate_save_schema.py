import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('vs',ROOT/'scripts/validate_save_schema.py')
MOD=importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(MOD)
class Tests(unittest.TestCase):
    def test_valid(self):
        d={"schema_version":3,"root_keys":["player","world","quests","settings"],"migrations":[{"from":1,"to":2},{"from":2,"to":3}],"atomic_write":True,"backup_slots":2,"unknown_key_policy":"preserve"}
        self.assertEqual(MOD.validate(d),[])
    def test_gap(self):
        d={"schema_version":3,"root_keys":["player"],"migrations":[{"from":1,"to":3}],"atomic_write":False,"backup_slots":0,"unknown_key_policy":"drop"}
        issues=MOD.validate(d)
        self.assertTrue(any("migration" in x.lower() for x in issues))
        self.assertTrue(any("atomic" in x.lower() for x in issues))
if __name__=='__main__': unittest.main()
