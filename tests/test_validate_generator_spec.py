import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('generator_validator',ROOT/'scripts/validate_generator_spec.py')

class GeneratorSpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(cls.mod)

    def valid_spec(self):
        return {
            'generator_id':'dungeon_v1','content_type':'room_graph',
            'seed_policy':{'deterministic':True,'record_seed':True,'record_state':True},
            'representation':'typed_room_graph',
            'hard_invariants':[{'id':'reachable_goal','description':'start必须可达goal'}],
            'generation_pipeline':['sample_skeleton','assign_room_roles','validate','repair','decorate'],
            'validation':{'checks':['reachable_goal'],'max_attempts':12},
            'repair_policy':['connect_unreachable_goal','replace_invalid_room'],
            'expressive_range_metrics':['linearity','branching','combat_density','recovery_spacing'],
            'fallbacks':['load_safe_authored_layout'],
            'random_tables':[{'id':'room_roles','entries':[{'id':'combat','weight':5},{'id':'reward','weight':2},{'id':'recovery','weight':1}]}]
        }

    def test_valid_spec_passes(self):
        self.assertEqual(self.mod.validate(self.valid_spec())['errors'],[])

    def test_uncovered_invariant_fails(self):
        spec=self.valid_spec(); spec['validation']['checks']=[]
        result=self.mod.validate(spec)
        self.assertTrue(any('not covered' in e for e in result['errors']))

    def test_unbounded_attempts_fail(self):
        spec=self.valid_spec(); spec['validation']['max_attempts']=0
        result=self.mod.validate(spec)
        self.assertTrue(any('max_attempts' in e for e in result['errors']))
