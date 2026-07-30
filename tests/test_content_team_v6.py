import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("dispatch_v6", ROOT / "scripts/build_dispatch_plan.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MOD)

class ContentTeamRoutingTests(unittest.TestCase):
    def test_quest_routes_narrative_and_tools(self):
        plan = MOD.build_plan({
            "content_tags": ["quest_graph", "branching_dialogue", "cutscene"],
            "technical_tags": ["save_state"],
            "needs_godot_implementation": True,
        })
        self.assertIn("narrative-quest-cinematics", plan["parallel_specialists"])
        self.assertIn("content-architecture-save-tools", plan["parallel_specialists"])
        self.assertTrue(any("quest" in item.lower() for item in plan["shared_dependencies"]))

    def test_enemy_ai_routes_ai_camera_and_godot(self):
        plan = MOD.build_plan({
            "content_tags": ["npc_ai", "perception", "behavior_tree", "combat_camera"],
            "needs_godot_implementation": True,
        })
        for agent in ["npc-ai-simulation", "gameplay-camera-composition", "godot-integration"]:
            self.assertIn(agent, plan["parallel_specialists"])

    def test_audio_content_routes_sound_not_only_music(self):
        plan = MOD.build_plan({"audio_tags": ["footstep_sfx", "foley", "voice_over", "spatial_audio"]})
        self.assertIn("sound-design-voice-mix", plan["parallel_specialists"])
        self.assertNotIn("interactive-music", plan["parallel_specialists"])

    def test_accessibility_localization_routes_specialist(self):
        plan = MOD.build_plan({"content_tags": ["subtitles", "input_remap", "reduced_motion", "localization"]})
        self.assertIn("ux-accessibility-localization", plan["parallel_specialists"])

    def test_asset_budget_routes_technical_art(self):
        plan = MOD.build_plan({"asset_tags": ["shader_budget", "lod", "overdraw", "texture_budget"]})
        self.assertIn("technical-art-rendering", plan["parallel_specialists"])

    def test_content_milestone_routes_production(self):
        plan = MOD.build_plan({"content_tags": ["vertical_slice", "content_scope", "milestone", "feature_freeze"]})
        self.assertEqual(plan["parallel_specialists"], ["content-production-scope"])

    def test_content_qa_is_postprocessing(self):
        plan = MOD.build_plan({"content_tags": ["quest_graph"], "needs_content_qa": True})
        self.assertIn("content-qa-automation", plan["postprocessing"])
        self.assertLess(plan["postprocessing"].index("content-qa-automation"), plan["postprocessing"].index("qa-acceptance"))

class ContractFileTests(unittest.TestCase):
    def test_new_contracts_exist(self):
        expected = [
            "agents/quest-spec.schema.json",
            "agents/npc-ai-spec.schema.json",
            "agents/content-budget.schema.json",
            "agents/accessibility-localization.schema.json",
            "agents/save-schema.schema.json",
        ]
        for rel in expected:
            self.assertTrue((ROOT / rel).is_file(), rel)
            json.loads((ROOT / rel).read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
