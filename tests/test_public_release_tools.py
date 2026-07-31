import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


def load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class PublicReleaseValidatorTests(unittest.TestCase):
    def test_relative_files_ignore_git_metadata(self):
        mod = load("validate_public_release_git", "scripts/validate_public_release.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git/objects").mkdir(parents=True)
            (root / ".git/objects/sample").write_bytes(b"\x00\xff")
            (root / "README.md").write_text("release", encoding="utf-8")
            relative = [path.relative_to(root).as_posix() for path in mod._relative_files(root)]
            self.assertEqual(["README.md"], relative)

    def test_public_release_has_required_files_and_no_forbidden_files(self):
        import shutil
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache, ignore_errors=True)
        mod = load("validate_public_release", "scripts/validate_public_release.py")
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache, ignore_errors=True)
        report = mod.validate_release(ROOT)
        self.assertEqual([], report["errors"])
        self.assertEqual(9, report["skills"])
        self.assertGreaterEqual(report["specialists"], 27)


class InstallDoctorTests(unittest.TestCase):
    def test_install_full_to_codex_layout_and_doctor_passes(self):
        installer = load("install_tool", "scripts/install.py")
        doctor = load("doctor_tool", "scripts/doctor.py")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            result = installer.install(ROOT, target, preset="full", target_runtime="codex")
            self.assertTrue((target / ".agents/skills/directing-godot-game-feel/SKILL.md").is_file())
            self.assertFalse((target / "AGENTS.md").exists())
            self.assertEqual(9, result["skills_installed"])
            self.assertEqual(28, result["codex_agents_installed"])
            report = doctor.inspect_installation(target)
            self.assertEqual([], report["errors"])
            self.assertEqual(9, report["skills_found"])
            self.assertEqual(28, report["codex_agents_found"])

    def test_install_presets_have_distinct_scopes(self):
        installer = load("install_presets", "scripts/install.py")
        doctor = load("doctor_presets", "scripts/doctor.py")
        expected = {
            "director": (1, True),
            "modules": (8, False),
            "full": (9, True),
        }
        for preset, (count, has_director) in expected.items():
            with self.subTest(preset=preset), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp)
                result = installer.install(
                    ROOT,
                    target,
                    preset=preset,
                    target_runtime="portable",
                )
                skills_root = target / ".agents/skills"
                self.assertEqual(count, result["skills_installed"])
                self.assertEqual(
                    has_director,
                    (skills_root / "directing-godot-game-feel/SKILL.md").is_file(),
                )
                self.assertEqual([], doctor.inspect_installation(target)["errors"])

    def test_agents_policy_is_opt_in_and_existing_file_is_preserved(self):
        installer = load("install_agents_policy", "scripts/install.py")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            installer.install(
                ROOT,
                target,
                preset="director",
                target_runtime="codex",
                write_agents_md=True,
            )
            policy = target / "AGENTS.md"
            self.assertTrue(policy.is_file())
            original = policy.read_text(encoding="utf-8")
            result = installer.install(
                ROOT,
                target,
                preset="director",
                target_runtime="codex",
                force=True,
                write_agents_md=True,
            )
            self.assertEqual(original, policy.read_text(encoding="utf-8"))
            self.assertFalse(result["agents_md_created"])

    def test_legacy_presets_resolve_to_canonical_scopes(self):
        installer = load("install_aliases", "scripts/install.py")
        aliases = {
            "core": "director",
            "skills-only": "modules",
            "godot-content-team": "full",
        }
        for alias, effective in aliases.items():
            with self.subTest(alias=alias), tempfile.TemporaryDirectory() as tmp:
                result = installer.install(
                    ROOT,
                    Path(tmp),
                    preset=alias,
                    target_runtime="portable",
                )
                self.assertEqual(effective, result["effective_preset"])

    def test_install_and_doctor_ignore_unrelated_project_extensions(self):
        installer = load("install_coexistence", "scripts/install.py")
        doctor = load("doctor_coexistence", "scripts/doctor.py")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            unrelated_skill = target / ".agents/skills/user-owned-skill/SKILL.md"
            unrelated_skill.parent.mkdir(parents=True)
            unrelated_skill.write_text("user-owned content\n", encoding="utf-8")
            unrelated_agent = target / ".codex/agents/user_owned.toml"
            unrelated_agent.parent.mkdir(parents=True)
            unrelated_agent.write_text("user-owned content\n", encoding="utf-8")

            result = installer.install(
                ROOT,
                target,
                preset="full",
                target_runtime="codex",
            )
            report = doctor.inspect_installation(target)

            self.assertEqual([], report["errors"])
            self.assertEqual(9, report["skills_found"])
            self.assertEqual(28, report["codex_agents_found"])
            self.assertEqual("user-owned content\n", unrelated_skill.read_text(encoding="utf-8"))
            self.assertEqual("user-owned content\n", unrelated_agent.read_text(encoding="utf-8"))
            self.assertEqual(28, len(result["codex_agent_names"]))


class ReleaseBuilderTests(unittest.TestCase):
    def test_release_builder_creates_zip_and_sha_file(self):
        mod = load("build_release", "scripts/build_release.py")
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            result = mod.build_release(ROOT, output, version="v0.1.0-alpha.1")
            self.assertTrue(result["archive"].is_file())
            self.assertTrue(result["checksums"].is_file())
            self.assertGreater(result["file_count"], 200)

    def test_package_manifest_matches_repository_contents(self):
        mod = load("package_manifest", "scripts/generate_package_manifest.py")
        actual = __import__("json").loads(
            (ROOT / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8")
        )
        self.assertEqual(mod.build_manifest(ROOT), actual)


class ReleaseWorkflowTests(unittest.TestCase):
    def test_workflows_pin_actions_and_run_live_godot_validation(self):
        validate = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
        release = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
        expected_pins = [
            "actions/checkout@11d5960a326750d5838078e36cf38b85af677262",
            "actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065",
        ]
        for workflow in (validate, release):
            for pin in expected_pins:
                self.assertIn(pin, workflow)
            self.assertIn("Godot_v4.6.3-stable_linux.x86_64.zip", workflow)
            self.assertIn(
                "d0bc2113065e481c9c2c2b2c37daa4e8be3fe9e27f0ab9ab0b6096e9a37907f3",
                workflow,
            )
            self.assertIn("scripts/run_godot_validation.py", workflow)
            self.assertIn('archive="$RUNNER_TEMP/$GODOT_ARCHIVE"', workflow)
            self.assertIn("GODOT_BIN=", workflow)

        self.assertIn(
            "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02",
            release,
        )
        self.assertIn(
            "actions/attest@508db95dd578ae2727ebd6217d5ba78e4fbda05d",
            release,
        )

    def test_publish_requires_existing_immutable_tag(self):
        release = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
        self.assertNotIn("git tag -a", release)
        self.assertNotIn("--clobber", release)
        self.assertIn('git rev-parse "${VERSION}^{commit}"', release)
        self.assertIn("Refusing to replace existing release", release)


if __name__ == "__main__":
    unittest.main()
