import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('dispatch',ROOT/'scripts/build_dispatch_plan.py')
MOD=importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(MOD)

class DispatchPlanTests(unittest.TestCase):
    def test_floating_walk_routes_motion_and_godot(self):
        plan=MOD.build_plan({'action_tags':['walk','turn'],'symptoms':['foot_sliding'],'needs_godot_implementation':True,'evidence_quality':'timestamped'})
        self.assertEqual(plan['mode'],'parallel_lite')
        self.assertEqual(plan['parallel_specialists'],['locomotion-grounding','godot-integration'])
        self.assertTrue(plan['shared_dependencies'])
        self.assertEqual(plan['postprocessing'][-1],'qa-acceptance')

    def test_gameplay_music_boss_routes_cross_discipline(self):
        plan=MOD.build_plan({'action_tags':['attack'],'gameplay_tags':['combat_loop','boss_phase'],'audio_tags':['adaptive_music','stinger'],'technical_tags':['animationtree','audio_bus','event_bus'],'needs_godot_implementation':True,'evidence_quality':'timestamped'})
        self.assertEqual(plan['mode'],'parallel_full')
        for agent in ['action-dynamics','gameplay-core-loop','encounter-pacing','interactive-music','godot-audio-integration','godot-integration']:
            self.assertIn(agent,plan['parallel_specialists'])
        self.assertTrue(any('encounter intensity' in x for x in plan['shared_dependencies']))

    def test_economy_only_does_not_start_motion_agents(self):
        plan=MOD.build_plan({'gameplay_tags':['economy','reward','progression'],'evidence_quality':'timestamped'})
        self.assertEqual(plan['parallel_specialists'],['systems-economy-progression'])
        self.assertNotIn('action-dynamics',plan['parallel_specialists'])

    def test_playtest_runs_after_synthesis(self):
        plan=MOD.build_plan({'gameplay_tags':['core_loop'],'has_playtest_data':True,'data_tags':['telemetry'],'evidence_quality':'timestamped'})
        self.assertEqual(plan['postprocessing'],['orchestrator-synthesis','playtest-analysis','qa-acceptance'])

    def test_vague_request_does_not_start_swarm(self):
        plan=MOD.build_plan({'symptoms':['stiff'],'evidence_quality':'unknown'})
        self.assertEqual(plan['mode'],'single'); self.assertEqual(plan['parallel_specialists'],[]); self.assertTrue(plan['warnings'])

    def test_level_design_routes_to_level_architecture(self):
        plan=MOD.build_plan({"gameplay_tags":["level_design","critical_path","landmark"]})
        self.assertIn("level-design-architecture",plan["parallel_specialists"])

    def test_balance_routes_to_balance_difficulty(self):
        plan=MOD.build_plan({"gameplay_tags":["difficulty_curve","challenge_budget","fairness"]})
        self.assertIn("balance-difficulty",plan["parallel_specialists"])

    def test_procgen_routes_to_generator_and_godot(self):
        plan=MOD.build_plan({"gameplay_tags":["procedural_generation","seed","random_level"],"needs_godot_implementation":True})
        self.assertIn("procedural-generation-randomness",plan["parallel_specialists"])
        self.assertIn("godot-integration",plan["parallel_specialists"])

    def test_roguelike_routes_minimal_relevant_team(self):
        plan=MOD.build_plan({"gameplay_tags":["roguelike","run_variation","loot_table","level_flow","difficulty_curve"]})
        chosen=set(plan["parallel_specialists"])
        self.assertTrue({"replayability-run-variation","systems-economy-progression","level-design-architecture","balance-difficulty"}.issubset(chosen))

if __name__=='__main__': unittest.main()
