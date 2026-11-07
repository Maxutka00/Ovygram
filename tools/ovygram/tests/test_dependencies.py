from pathlib import Path
import sys
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "Telegram/PluginSDK"))

from ovygram_deps import Dependencies, normalize, normalize_all
from ovygram_runtime import Manager, read_metadata


class FakePip:
    """Installs "name==version" requirements as tiny packages, like pip
    with --target would, or fails with a pip-like message."""

    def __init__(self):
        self.calls = []
        self.fail = None

    def __call__(self, command, environment, log_path):
        self.calls.append(command)
        if self.fail:
            return 1, f"Collecting x\nERROR: {self.fail}\n"
        target = Path(command[command.index("--target") + 1])
        for requirement in command[command.index("--") + 1:]:
            name, version = requirement.split("==")
            module = name.replace("-", "_")
            (target / module).mkdir()
            (target / module / "__init__.py").write_text(f"VERSION = {version!r}\n")
            info = target / f"{module}-{version}.dist-info"
            info.mkdir()
            (info / "METADATA").write_text(
                f"Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n")
        return 0, "Successfully installed\n"


def plugin_source(identity, requirements, module):
    return (
        "from base_plugin import BasePlugin\n"
        f"__id__ = {identity!r}\n__name__ = 'Test'\n__version__ = '1.0'\n"
        "__author__ = 'Test'\n__description__ = 'Test'\n"
        "__platform__ = 'desktop'\n__desktop_sdk__ = 2\n"
        f"__requirements__ = {requirements!r}\n"
        "class TestPlugin(BasePlugin):\n"
        "    def on_plugin_load(self):\n"
        f"        import {module}\n"
        f"        self.version = {module}.VERSION\n")


class RequirementTests(unittest.TestCase):
    def test_requirements_are_normalized(self):
        self.assertEqual(normalize("Requests >= 2.31 , <3"), "requests>=2.31,<3")
        self.assertEqual(normalize("PyYAML[Libyaml,c_ext]==6.0.2"), "pyyaml[c-ext,libyaml]==6.0.2")
        self.assertEqual(normalize_all(["b", "a", "A"]), ["a", "b"])

    def test_only_names_and_versions_are_accepted(self):
        for bad in ("-e .", "--index-url=http://x", "pkg @ https://x/y.whl", "./local",
                    "pkg; sys_platform == 'win32'", "", "pkg==1 extra", "x" * 201):
            with self.assertRaises(ValueError, msg=bad):
                normalize(bad)
        with self.assertRaises(ValueError):
            normalize_all("requests")
        with self.assertRaises(ValueError):
            normalize_all([f"p{i}" for i in range(33)])

    def test_metadata_keeps_requirements_absent_when_not_declared(self):
        base = ("__id__ = 'a.b'\n__name__ = 'A'\n__version__ = '1'\n__author__ = 'A'\n"
                "__description__ = 'A'\n__platform__ = 'desktop'\n__desktop_sdk__ = 2\n")
        self.assertNotIn("requirements", read_metadata(base.encode(), "x"))
        values = read_metadata((base + "__requirements__ = ['Six==1.17']\n").encode(), "x")
        self.assertEqual(values["requirements"], ["six==1.17"])


class ExampleTests(unittest.TestCase):
    def test_qr_example_declares_its_libraries(self):
        source = (ROOT / "tools/ovygram/examples/qr_code.plugin").read_bytes()
        self.assertEqual(read_metadata(source, "qr_code.plugin")["requirements"],
                         ["pillow>=11", "qrcode[pil]>=8.2,<9"])


class DependencyManagerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.pip = FakePip()
        self.paths = list(sys.path)
        self.addCleanup(self.restore_path)
        self.manager = self.new_manager()

    def restore_path(self):
        sys.path[:] = self.paths
        for name in [name for name in sys.modules if name.startswith("fakepkg")]:
            del sys.modules[name]

    def new_manager(self):
        manager = Manager(self.root / "profile")
        manager.dependencies.runner = self.pip
        manager.dependencies.interpreter = lambda: (["python", "pip.whl/pip"], {})
        self.addCleanup(manager.shutdown)
        return manager

    def install(self, identity, requirements, module="fakepkg"):
        source = self.root / f"{identity}.plugin"
        source.write_text(plugin_source(identity, requirements, module), encoding="utf-8")
        return self.manager.install(str(source))

    def wait(self, manager=None):
        manager = manager or self.manager
        for _ in range(500):
            if not manager.dependencies.installing():
                break
            time.sleep(0.01)
        manager.dispatch('{"action": "snapshot"}')

    def test_enable_installs_and_then_starts_the_plugin(self):
        plugin_id = self.install("dep.a", ["fakepkg==1.0"])
        self.manager.enable(plugin_id)
        snapshot = self.manager.snapshot()
        self.assertTrue(snapshot["plugins"][0]["enabled"])
        self.wait()
        self.assertIn(plugin_id, self.manager.loaded)
        self.assertEqual(self.manager.loaded[plugin_id][0].version, "1.0")
        command = self.pip.calls[0]
        self.assertIn("--only-binary=:all:", command)
        self.assertEqual(command[command.index("--") + 1:], ["fakepkg==1.0"])
        self.assertEqual(self.manager.snapshot()["dependencies"]["packages"], {"fakepkg": "1.0"})

    def test_satisfied_requirements_start_without_pip(self):
        first = self.install("dep.a", ["fakepkg==1.0"])
        self.manager.enable(first)
        self.wait()
        second = self.install("dep.b", ["fakepkg==1.0"])
        self.manager.enable(second)
        self.assertIn(second, self.manager.loaded)
        self.assertEqual(len(self.pip.calls), 1)

    def test_changed_version_waits_for_the_restart(self):
        first = self.install("dep.a", ["fakepkg==1.0"])
        self.manager.enable(first)
        self.wait()
        # Only enabled plugins take part in the resolution, so the version
        # in use changes, and it can't change in a running process.
        self.manager.disable(first)
        second = self.install("dep.b", ["fakepkg==2.0"])
        self.manager.enable(second)
        self.wait()
        self.assertNotIn(second, self.manager.loaded)
        self.assertEqual(self.manager.errors[second], "Зависимости установлены. Перезапустите клиент.")
        self.assertTrue(self.manager.snapshot()["dependencies"]["restart"])
        self.assertTrue(self.manager.records[second]["enabled"])

        self.manager.shutdown()
        self.restore_path()
        restarted = self.new_manager()
        self.assertFalse(restarted.snapshot()["dependencies"]["restart"])
        self.assertEqual(restarted.loaded[second][0].version, "2.0")
        directories = [path for path in (self.root / "profile/dependencies").iterdir() if path.is_dir()]
        self.assertEqual(len(directories), 1)

    def test_pip_failure_disables_the_plugin_with_the_reason(self):
        self.pip.fail = "ResolutionImpossible: conflicting versions"
        plugin_id = self.install("dep.a", ["fakepkg==1.0"])
        self.manager.enable(plugin_id)
        self.wait()
        self.assertNotIn(plugin_id, self.manager.loaded)
        self.assertFalse(self.manager.records[plugin_id]["enabled"])
        self.assertIn("ResolutionImpossible", self.manager.errors[plugin_id])

    def test_one_installation_at_a_time(self):
        def slow(command, environment, log_path):
            time.sleep(0.3)
            return self.pip(command, environment, log_path)

        self.manager.dependencies.runner = slow
        first = self.install("dep.a", ["fakepkg==1.0"])
        second = self.install("dep.b", ["fakepkg-two==1.0"], module="fakepkg_two")
        self.manager.enable(first)
        with self.assertRaises(RuntimeError):
            self.manager.enable(second)
        self.wait()
        self.assertIn(first, self.manager.loaded)

    def test_missing_pip_is_reported(self):
        dependencies = Dependencies(self.root / "other", self.root / "no-python")
        with self.assertRaises(RuntimeError):
            dependencies.install("x", ["fakepkg==1.0"], lambda error: None)


if __name__ == "__main__":
    unittest.main()
