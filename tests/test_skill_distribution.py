import importlib.util
import json
import tempfile
import tomllib
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]
DIRECTOR = "directing-godot-game-feel"
REQUIRED_EVAL_CATEGORIES = {"direct", "indirect", "incomplete", "negative"}


def load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def skill_dirs() -> list[Path]:
    return sorted(path.parent for path in (ROOT / "skills").glob("*/SKILL.md"))


class SkillDistributionTests(unittest.TestCase):
    def test_plugin_manifest_and_skill_metadata_are_complete(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual("godot-game-development-director", manifest["name"])
        self.assertEqual("0.1.0-alpha.1", manifest["version"])
        self.assertEqual("./skills/", manifest["skills"])

        self.assertEqual(9, len(skill_dirs()))
        for skill_dir in skill_dirs():
            with self.subTest(skill=skill_dir.name):
                metadata = yaml.safe_load(
                    (skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")
                )
                interface = metadata["interface"]
                self.assertGreaterEqual(len(interface["short_description"]), 25)
                self.assertLessEqual(len(interface["short_description"]), 64)
                self.assertIn(f"${skill_dir.name}", interface["default_prompt"])

    def test_each_skill_has_balanced_trigger_evals(self):
        for skill_dir in skill_dirs():
            with self.subTest(skill=skill_dir.name):
                payload = json.loads((skill_dir / "evals/evals.json").read_text(encoding="utf-8"))
                self.assertEqual(skill_dir.name, payload["skill_name"])
                categories = {item["category"] for item in payload["evals"]}
                self.assertEqual(REQUIRED_EVAL_CATEGORIES, categories)
                for item in payload["evals"]:
                    self.assertTrue(item["prompt"].strip())
                    self.assertTrue(item["expected_output"].strip())

    def test_all_documented_skill_relative_paths_exist(self):
        validator = load("skill_reference_validator", "scripts/validate_skill_references.py")
        checked = [ROOT, *skill_dirs()]
        failures = {}
        for skill_dir in checked:
            errors = validator.validate_skill_directory(skill_dir)
            if errors:
                failures[str(skill_dir)] = errors
        self.assertEqual({}, failures)

    def test_reference_validator_detects_missing_file(self):
        validator = load("skill_reference_negative", "scripts/validate_skill_references.py")
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp)
            (skill / "SKILL.md").write_text(
                "---\n"
                "name: broken-skill\n"
                "description: Use when testing a missing reference.\n"
                "---\n\n"
                "Read `references/missing.md` before acting.\n",
                encoding="utf-8",
            )
            errors = validator.validate_skill_directory(skill)
            self.assertEqual(1, len(errors))
            self.assertIn("references/missing.md", errors[0])

    def test_director_source_and_plugin_entrypoint_match(self):
        self.assertEqual(
            (ROOT / "SKILL.md").read_text(encoding="utf-8"),
            (ROOT / f"skills/{DIRECTOR}/SKILL.md").read_text(encoding="utf-8"),
        )

    def test_generated_codex_agents_are_valid_project_agents(self):
        generator = load("codex_agent_generator", "scripts/generate_codex_agents.py")
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)
            result = generator.generate_agents(ROOT, destination)
            self.assertEqual(28, result["agents_generated"])
            for path in sorted(destination.glob("*.toml")):
                with self.subTest(agent=path.name):
                    payload = tomllib.loads(path.read_text(encoding="utf-8"))
                    self.assertTrue(payload["name"])
                    self.assertTrue(payload["description"])
                    self.assertTrue(payload["developer_instructions"])

    def test_godot_fixture_covers_every_shipped_gdscript(self):
        fixture = (ROOT / "tests/godot_fixture/validate_package_scripts.gd").read_text(
            encoding="utf-8"
        )
        shipped = sorted(path.name for path in (ROOT / "scripts").glob("*.gd"))
        self.assertGreaterEqual(len(shipped), 9)
        for filename in shipped:
            with self.subTest(script=filename):
                self.assertIn(filename, fixture)


if __name__ == "__main__":
    unittest.main()
