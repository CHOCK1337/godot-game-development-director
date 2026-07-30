import importlib.util, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('ac',ROOT/'scripts/audit_content_coverage.py')
MOD=importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(MOD)
class Tests(unittest.TestCase):
    def test_complete(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.csv'; p.write_text('content_id,category,status,owner,test_status\na,quest,done,n,pass\n',encoding='utf-8')
            self.assertTrue(MOD.audit(p)['complete'])
    def test_detects_gaps(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.csv'; p.write_text('content_id,category,status,owner,test_status\na,quest,blocked,,fail\na,quest,done,x,pass\n',encoding='utf-8')
            r=MOD.audit(p); self.assertFalse(r['complete']); self.assertEqual(r['duplicate_ids'],['a']); self.assertEqual(r['missing_owner'],['a'])
if __name__=='__main__': unittest.main()
