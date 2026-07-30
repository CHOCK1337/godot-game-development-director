import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('level_validator',ROOT/'scripts/validate_level_spec.py')

class LevelSpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(cls.mod)

    def valid_spec(self):
        return {
            'experience_goal':'玩家通过观察地标和敌人配置，在风险路线与安全路线间作出选择',
            'level_type':'2d_action_roguelite',
            'player_capabilities':['move','dash','attack'],
            'topology':{'nodes':[{'id':'start','kind':'start'},{'id':'arena','kind':'combat'},{'id':'rest','kind':'recovery'},{'id':'boss','kind':'goal'}],
                        'edges':[{'from':'start','to':'arena'},{'from':'arena','to':'rest'},{'from':'rest','to':'boss'}]},
            'critical_path':['start','arena','rest','boss'],
            'optional_routes':[],
            'intensity_curve':[{'segment':'start','intensity':1},{'segment':'arena','intensity':7},{'segment':'rest','intensity':3},{'segment':'boss','intensity':9}],
            'landmarks':[{'id':'tower','purpose':'orientation'}],
            'gates':[],
            'hard_invariants':['start_reaches_goal','all_required_rooms_reachable'],
            'playtest_hypotheses':[{'hypothesis':'玩家能在30秒内判断主路方向','measure':'wrong_turn_rate','falsifier':'超过30%玩家首次进入死路'}]
        }

    def test_valid_spec_passes(self):
        result=self.mod.validate(self.valid_spec())
        self.assertEqual(result['errors'],[])

    def test_disconnected_critical_path_fails(self):
        spec=self.valid_spec(); spec['topology']['edges'].pop()
        result=self.mod.validate(spec)
        self.assertTrue(any('critical_path edge missing' in e for e in result['errors']))

    def test_curve_without_recovery_warns(self):
        spec=self.valid_spec(); spec['intensity_curve']=[{'segment':'a','intensity':1},{'segment':'b','intensity':4},{'segment':'c','intensity':8}]
        result=self.mod.validate(spec)
        self.assertTrue(any('recovery' in w for w in result['warnings']))
