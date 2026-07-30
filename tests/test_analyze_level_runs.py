import csv, importlib.util, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('level_runs',ROOT/'scripts/analyze_level_runs.py')
MOD=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)

class LevelRunAnalysisTests(unittest.TestCase):
    def test_reports_seed_outlier_hotspot_and_diversity(self):
        rows=[
            {'run_id':'1','seed':'10','completed':'1','duration_s':'100','deaths':'0','death_room':'','path_signature':'A-B-C'},
            {'run_id':'2','seed':'10','completed':'1','duration_s':'110','deaths':'1','death_room':'B','path_signature':'A-B-C'},
            {'run_id':'3','seed':'99','completed':'0','duration_s':'80','deaths':'4','death_room':'X','path_signature':'A-X'},
            {'run_id':'4','seed':'99','completed':'0','duration_s':'75','deaths':'5','death_room':'X','path_signature':'A-X'},
        ]
        with tempfile.NamedTemporaryFile('w',newline='',delete=False,encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows); path=Path(f.name)
        result=MOD.analyze(path)
        self.assertIn('99',result['seed_outliers'])
        self.assertEqual(result['death_hotspots'][0]['room'],'X')
        self.assertEqual(result['unique_path_count'],2)
