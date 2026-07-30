import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('random_audit',ROOT/'scripts/audit_random_table.py')
MOD=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)

class RandomTableTests(unittest.TestCase):
    def test_balanced_table_has_no_errors(self):
        table={'id':'rewards','entries':[{'id':'a','weight':3},{'id':'b','weight':2},{'id':'c','weight':1}], 'policy':{'max_repeat':2}}
        result=MOD.audit(table)
        self.assertEqual(result['errors'],[])
        self.assertAlmostEqual(sum(x['probability'] for x in result['normalized']),1.0)

    def test_zero_weight_and_duplicate_fail(self):
        table={'id':'bad','entries':[{'id':'a','weight':0},{'id':'a','weight':2}]}
        result=MOD.audit(table)
        self.assertTrue(any('duplicate' in e for e in result['errors']))
        self.assertTrue(any('positive' in e for e in result['errors']))

    def test_dominant_entry_without_streak_control_warns(self):
        table={'id':'dominant','entries':[{'id':'a','weight':9},{'id':'b','weight':1}]}
        result=MOD.audit(table)
        self.assertTrue(any('dominant' in w for w in result['warnings']))
