import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[3]
EXAMPLE = ROOT / "tools/ovygram/examples/lifecycle.ovyplugin"
sys.path.insert(0, str(ROOT / "Telegram/PluginSDK"))
from ovygram_runtime import Manager


class PluginRuntimeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.profile = self.root / "profile"

    def test_import_does_not_execute_plugin(self):
        manager = Manager(self.profile)
        self.addCleanup(manager.shutdown)
        source = self.root / "lifecycle.ovyplugin"
        source.write_text(EXAMPLE.read_text(encoding="utf-8") + '\nraise SystemExit("test")\n',
                          encoding="utf-8")
        plugin_id = manager.install(str(source))
        self.assertFalse(manager.snapshot()["plugins"][0]["enabled"])
        with self.assertRaisesRegex(RuntimeError, "test"):
            manager.enable(plugin_id)
        status = manager.snapshot()["plugins"][0]
        self.assertFalse(status["loaded"])
        self.assertFalse(status["enabled"])
        self.assertEqual(status["error"], "test")

    def test_restart_and_crash_recovery_keep_settings(self):
        manager = Manager(self.profile)
        try:
            plugin_id = manager.install(str(EXAMPLE))
            manager.enable(plugin_id)
            manager.save_settings(plugin_id, {"enabled_example": True, "greeting": "Сохранено", "choice": 1})
        finally:
            manager.shutdown()
        self.profile.joinpath("running").write_text(plugin_id, encoding="utf-8")
        recovery = Manager(self.profile)
        self.addCleanup(recovery.shutdown)
        self.assertTrue(recovery.snapshot()["recovery"])
        self.assertFalse(recovery.loaded)
        recovery.resume()
        recovery.resume()
        self.assertEqual(recovery.records[plugin_id]["settings"]["load_count"], 2)
        self.assertEqual(recovery.settings(plugin_id)[1]["value"], "Сохранено")
        recovery.disable(plugin_id)
        self.assertFalse(recovery.loaded)

    def test_zip_resources_and_rollback(self):
        manager = Manager(self.profile)
        self.addCleanup(manager.shutdown)
        plugin_id = manager.install(str(EXAMPLE))
        manager.records[plugin_id]["current"].pop("share_file")
        # Simulate a pre-hash installation, whose original package wasn't kept.
        manager.records[plugin_id]["current"].pop("sha256")
        archive = self.root / "lifecycle.ovyzip"
        source = EXAMPLE.read_text(encoding="utf-8").replace("1.0.0", "2.0.0")
        with zipfile.ZipFile(archive, "w") as package:
            package.writestr("plugin.json", '{"id": "lifecycle", "entry": "main.py"}')
            package.writestr("main.py", source + "\nfrom .resource import value\n")
            package.writestr("resource.py", "value = 5\n")
        manager.install(str(archive), plugin_id)
        manager.enable(plugin_id)
        self.assertEqual(manager.snapshot()["plugins"][0]["version"], "2.0.0")
        current = manager.records[plugin_id]["current"]
        manager.directory(current).joinpath("runtime-private.txt").write_text("local data")
        shared = Path(json.loads(manager.dispatch(json.dumps({
            "action": "share_file", "installation_id": plugin_id,
        })))["result"])
        self.assertEqual(shared.name, "lifecycle.ovyzip")
        self.assertEqual(shared.read_bytes(), archive.read_bytes())
        manager.rollback(plugin_id)
        self.assertEqual(manager.snapshot()["plugins"][0]["version"], "1.0.0")
        self.assertFalse(manager.loaded)
        legacy_file = Path(manager.share_file(plugin_id))
        self.assertEqual(legacy_file.read_bytes(), EXAMPLE.read_bytes())
        manager.remove(plugin_id)
        self.assertEqual(manager.snapshot()["plugins"], [])
        self.assertFalse(shared.exists())
        self.assertFalse(legacy_file.exists())

    def test_zip_with_windows_path_escape_is_rejected(self):
        manager = Manager(self.profile)
        self.addCleanup(manager.shutdown)
        for path in ("../escape", "c:/escape", "aux.txt", "a\\escape"):
            with self.subTest(path=path):
                archive = self.root / "lifecycle.ovyzip"
                with zipfile.ZipFile(archive, "w") as package:
                    package.writestr("plugin.json", '{"id": "lifecycle", "entry": "main.py"}')
                    package.write(EXAMPLE, "main.py")
                    package.writestr(path.replace("\\", "/"), "bad")
                if "\\" in path:
                    # ZipInfo normalizes names when writing on Windows.
                    archive.write_bytes(archive.read_bytes().replace(
                        path.replace("\\", "/").encode(), path.encode()))
                with self.assertRaises(ValueError):
                    manager.install(str(archive))
                self.assertEqual(list(manager.packages.iterdir()), [])

    @unittest.skipUnless(os.environ.get("OVYGRAM_SMOKE_EXE"), "native host not staged")
    def test_embedded_host_loads_and_restarts(self):
        executable = Path(os.environ["OVYGRAM_SMOKE_EXE"])

        def run(*requests, disabled=False):
            result = subprocess.run(
                [str(executable), str(self.profile), "disabled" if disabled else "normal"],
                input="\n".join(json.dumps(request) for request in requests) + "\n",
                text=True, encoding="utf-8", capture_output=True, timeout=30,
                cwd=self.root,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            responses = [json.loads(line) for line in result.stdout.splitlines()]
            self.assertEqual(len(responses), len(requests))
            self.assertTrue(all("result" in response for response in responses), responses)
            return [response["result"] for response in responses]

        installation_id = run({"action": "install", "path": str(EXAMPLE)})[0]
        first = run(
            {"action": "enable", "installation_id": installation_id},
            {"action": "snapshot"},
        )
        self.assertTrue(first[-1]["plugins"][0]["loaded"])
        self.assertFalse(self.profile.joinpath("running").exists())
        self.assertFalse(run({"action": "snapshot"}, disabled=True)[0]["plugins"][0]["loaded"])
        self.assertTrue(run({"action": "snapshot"})[0]["plugins"][0]["loaded"])
        state = json.loads(self.profile.joinpath("state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["installations"][installation_id]["settings"]["load_count"], 2)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.profile = self.root / "profile"
        self.manager = Manager(self.profile)
        self.addCleanup(self.manager.shutdown)
        self.manager.runtime.sender = lambda command: None

    def copy(self, name="lifecycle.ovyplugin", version=None):
        source = self.root / "files" / name
        source.parent.mkdir(exist_ok=True)
        text = EXAMPLE.read_text(encoding="utf-8")
        source.write_text(text.replace('"1.0.0"', repr(version).replace("'", '"')) if version else text,
                          encoding="utf-8")
        return source

    def test_inspect_does_not_install(self):
        info = self.manager.inspect(str(self.copy()))
        self.assertEqual(info["metadata"]["id"], "lifecycle")
        self.assertEqual(info["package_type"], "ovyplugin")
        self.assertEqual(len(info["sha256"]), 64)
        self.assertEqual(info["installations"], [])
        self.assertEqual(self.manager.records, {})

    def test_setting_headers_and_buttons_keep_owner_and_reject_stale_clicks(self):
        source = self.root / "settings_actions.ovyplugin"
        source.write_text('''from base_plugin import BasePlugin
from ui.settings import Button, Header, Input
__id__ = "settings_actions"
__name__ = "Settings actions"
__description__ = "Settings action test"
__author__ = "Test"
__version__ = "1.0"
__release__ = False
__platform__ = "desktop"
__desktop_sdk__ = 2
class SettingsPlugin(BasePlugin):
    def create_settings(self):
        return [Header("Section"), Button("action", "Run", self.clicked), Input("name", "Name", "Default")]
    def clicked(self):
        self.set_setting("clicked", self.get_setting("clicked", 0) + 1)
''', encoding="utf-8")
        first = self.manager.install(str(source))
        second = self.manager.install(str(source), separate=True)
        self.manager.enable(first)
        self.manager.enable(second)
        fields = self.manager.settings(first)
        self.assertEqual([field["kind"] for field in fields], ["header", "button", "input"])
        action = fields[1]["action_id"]
        with self.assertRaisesRegex(ValueError, "устарела"):
            self.manager.settings_action(second, action)
        self.manager.save_settings(first, {"name": "Changed"})
        self.manager.settings_action(first, action)
        self.assertEqual(self.manager.records[first]["settings"]["clicked"], 1)
        self.assertNotIn("clicked", self.manager.records[second]["settings"])
        self.manager.disable(first)
        self.manager.enable(first)
        with self.assertRaisesRegex(ValueError, "устарела"):
            self.manager.settings_action(first, action)

    def test_two_installations_of_one_id_are_isolated(self):
        first = self.manager.install(str(self.copy()))
        with self.assertRaisesRegex(ValueError, "отдельно"):
            self.manager.install(str(self.copy()))
        second = self.manager.install(str(self.copy()), separate=True)
        self.assertNotEqual(first, second)
        for installation_id in (first, second):
            self.manager.enable(installation_id)
        self.manager.save_settings(first, {"enabled_example": True, "greeting": "первый", "choice": 1})
        self.assertNotEqual(self.manager.settings(second)[1]["value"], "первый")
        self.manager.runtime.contexts[first].set("only_first", 1)
        self.assertNotIn("only_first", self.manager.records[second]["settings"])
        self.assertEqual({plugin["instances"] for plugin in self.manager.snapshot()["plugins"]}, {2})
        self.assertEqual(len(self.manager.inspect(str(self.copy()))["installations"]), 2)

    def test_update_keeps_the_installation(self):
        installation_id = self.manager.install(str(self.copy()))
        self.manager.enable(installation_id)
        data = self.profile / "data" / installation_id
        data.mkdir(parents=True)
        (data / "notes.txt").write_text("keep")
        updated = self.manager.install(str(self.copy(version="1.1")), installation_id)
        self.assertEqual(updated, installation_id)
        self.assertEqual(self.manager.records[installation_id]["settings"]["load_count"], 1)
        self.assertTrue((data / "notes.txt").exists())
        self.assertEqual(self.manager.describe(installation_id)["version"], "1.1")
        self.manager.remove(installation_id)
        self.assertFalse(data.exists())

    def test_replaced_files_are_not_loaded(self):
        installation_id = self.manager.install(str(self.copy()))
        version = self.manager.records[installation_id]["current"]
        entry = self.manager.directory(version) / "plugin.py"
        entry.write_text(entry.read_text(encoding="utf-8") + "\n# changed\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "изменён"):
            self.manager.enable(installation_id)
        self.assertNotIn(installation_id, self.manager.loaded)

    def test_legacy_state_is_migrated(self):
        self.manager.shutdown()
        legacy = self.root / "legacy"
        packages = legacy / "packages" / ("a" * 32)
        packages.mkdir(parents=True)
        source = EXAMPLE.read_text(encoding="utf-8").replace(
            '__id__ = "lifecycle"', '__id__ = "desktop.lifecycle"').replace("__release__ = False\n", "")
        (packages / "plugin.py").write_text(source, encoding="utf-8")
        (legacy / "data" / "desktop.lifecycle").mkdir(parents=True)
        (legacy / "data" / "desktop.lifecycle" / "notes.txt").write_text("keep")
        from ovygram_runtime import legacy_metadata
        metadata = legacy_metadata(source.encode(), "plugin.py")
        (legacy / "state.json").write_text(json.dumps({"desktop.lifecycle": {
            "current": {"directory": "a" * 32, "metadata": metadata, "entry": "plugin.py"},
            "previous": None, "enabled": True, "settings": {"load_count": 5},
        }}), encoding="utf-8")
        manager = Manager(legacy)
        self.addCleanup(manager.shutdown)
        manager.runtime.sender = lambda command: None
        [(installation_id, record)] = manager.records.items()
        self.assertEqual(record["plugin_id"], "desktop.lifecycle")
        self.assertIn(installation_id, manager.loaded, manager.errors)
        self.assertEqual(record["settings"]["load_count"], 6)
        self.assertTrue((legacy / "data" / installation_id / "notes.txt").exists())
        state = json.loads((legacy / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(list(state["installations"]), [installation_id])
