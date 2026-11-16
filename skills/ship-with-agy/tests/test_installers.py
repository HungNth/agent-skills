"""Exercise installer commands against isolated configuration directories."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SKILL = Path(__file__).resolve().parents[1]


class Installers(unittest.TestCase):
    def exercise(self, command, variable, force):
        with tempfile.TemporaryDirectory(prefix="herdr-install-") as directory:
            config = Path(directory) / "config with spaces"
            env = dict(os.environ, **{variable: config.as_posix()})
            env["PATH"] = str(Path(command[0]).parent) + os.pathsep + env.get("PATH", "")
            target = config / "herdr-core/templates/agy-implementer.md"
            source = SKILL / "templates/agy-implementer.md"

            def run(*args):
                return subprocess.run(command + list(args), env=env, capture_output=True, text=True)

            result = run()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(target.read_bytes(), source.read_bytes())
            modified = target.stat().st_mtime_ns
            self.assertEqual(run().returncode, 0)
            self.assertEqual(target.stat().st_mtime_ns, modified)
            sibling = target.with_name("custom.md")
            sibling.write_text("keep")
            target.write_text("customized")
            self.assertNotEqual(run().returncode, 0)
            self.assertEqual(target.read_text(), "customized")
            self.assertEqual(run(force).returncode, 0)
            self.assertEqual(target.read_bytes(), source.read_bytes())
            self.assertEqual(sibling.read_text(), "keep")
            self.assertNotEqual(run("--unknown").returncode, 0)
            target.unlink()
            target.mkdir()
            self.assertNotEqual(run(force).returncode, 0)
            self.assertEqual(list(target.iterdir()), [])

    def test_powershell(self):
        shell = shutil.which("pwsh") or shutil.which("powershell")
        self.assertIsNotNone(shell, "PowerShell required")
        self.exercise([shell, "-NoProfile", "-File", str(SKILL / "scripts/install-herdr-templates.ps1")], "APPDATA", "-Force")

    def test_posix(self):
        shell = os.environ.get("TEST_SH") or shutil.which("sh")
        self.assertIsNotNone(shell, "Set TEST_SH to a POSIX shell")
        self.exercise([shell, (SKILL / "scripts/install-herdr-templates.sh").as_posix()], "XDG_CONFIG_HOME", "--force")


if __name__ == "__main__":
    unittest.main()
