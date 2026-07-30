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
    def test_public_release_has_required_files_and_no_forbidden_files(self):
        import shutil
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache, ignore_errors=True)
        mod = load("validate_public_release", "scripts/validate_public_release.py")
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache, ignore_errors=True)
        report = mod.validate_release(ROOT)
        self.assertEqual([], report["errors"])
        self.assertGreaterEqual(report["skills"], 8)
        self.assertGreaterEqual(report["specialists"], 27)


class InstallDoctorTests(unittest.TestCase):
    def test_install_core_to_codex_layout_and_doctor_passes(self):
        installer = load("install_tool", "scripts/install.py")
        doctor = load("doctor_tool", "scripts/doctor.py")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            result = installer.install(ROOT, target, preset="godot-content-team", target_runtime="codex")
            self.assertTrue((target / ".agents/skills/directing-godot-game-feel/SKILL.md").is_file())
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertGreaterEqual(result["copied_files"], 10)
            report = doctor.inspect_installation(target)
            self.assertEqual([], report["errors"])
            self.assertGreaterEqual(report["skills_found"], 8)


class ReleaseBuilderTests(unittest.TestCase):
    def test_release_builder_creates_zip_and_sha_file(self):
        mod = load("build_release", "scripts/build_release.py")
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            result = mod.build_release(ROOT, output, version="v0.1.0-alpha")
            self.assertTrue(result["archive"].is_file())
            self.assertTrue(result["checksums"].is_file())
            self.assertGreater(result["file_count"], 200)


if __name__ == "__main__":
    unittest.main()
