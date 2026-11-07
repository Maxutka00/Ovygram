from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "tools/ovygram/package_linux.py"


class PackageLinuxTests(unittest.TestCase):
    def make_build(self, directory, complete=True):
        build = Path(directory) / "build"
        (build / "python/sdk").mkdir(parents=True)
        (build / "Ovygram").write_bytes(b"binary")
        names = ["ovygram_host.so", "python313.zip", "sdk/ovygram_runtime.py", "sdk/ovygram_deps.py"]
        if complete:
            names.append("pip.whl")
        for name in names:
            (build / "python" / name).write_text("x")
        (build / "python/sdk/__pycache__").mkdir()
        (build / "python/sdk/__pycache__/x.pyc").write_text("x")
        return build

    def run_script(self, build, output):
        return subprocess.run([sys.executable, str(SCRIPT), "--build", str(build),
                               "--output", str(output), "--no-strip"],
                              capture_output=True, text=True)

    def test_archive_layout(self):
        with tempfile.TemporaryDirectory() as directory:
            build = self.make_build(directory)
            result = self.run_script(build, Path(directory) / "dist")
            self.assertEqual(result.returncode, 0, result.stderr)
            archive = Path(result.stdout.splitlines()[0])
            with tarfile.open(archive) as tar:
                names = set(tar.getnames())
            prefix = archive.name.removesuffix(".tar.xz")
            for name in ("Ovygram", "LICENSE", "io.github.maxutka00.Ovygram.desktop",
                         "python/pip.whl", "python/sdk/ovygram_deps.py",
                         "icons/hicolor/256x256/apps/io.github.maxutka00.Ovygram.png",
                         "icons/hicolor/symbolic/apps/io.github.maxutka00.Ovygram-symbolic.svg",
                         "icons/hicolor/symbolic/apps/io.github.maxutka00.Ovygram-mute-symbolic.svg"):
                self.assertIn(f"{prefix}/{name}", names)
            self.assertFalse(any("__pycache__" in name for name in names))
            self.assertTrue(archive.with_name(archive.name + ".sha256").exists())

    def test_stale_runtime_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_script(self.make_build(directory, complete=False), Path(directory) / "dist")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("pip.whl", result.stderr)


if __name__ == "__main__":
    unittest.main()
