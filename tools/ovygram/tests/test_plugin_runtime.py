import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[3]
EXAMPLE = ROOT / "tools/ovygram/examples/lifecycle.plugin"
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
        source = self.root / "bad.py"
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
        archive = self.root / "new.zip"
        source = EXAMPLE.read_text(encoding="utf-8").replace("1.0.0", "2.0.0")
        with zipfile.ZipFile(archive, "w") as package:
            package.writestr("plugin.json", '{"entry":"main.py"}')
            package.writestr("main.py", source + "\nfrom .resource import value\n")
            package.writestr("resource.py", "value = 5\n")
        manager.install(str(archive), plugin_id)
        manager.enable(plugin_id)
        self.assertEqual(manager.snapshot()["plugins"][0]["version"], "2.0.0")
        current = manager.records[plugin_id]["current"]
        manager.directory(current).joinpath("runtime-private.txt").write_text("local data")
        shared = Path(json.loads(manager.dispatch(json.dumps({
            "action": "share_file", "plugin_id": plugin_id,
        })))["result"])
        self.assertEqual(shared.suffix, ".zip")
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
                archive = self.root / "bad.zip"
                with zipfile.ZipFile(archive, "w") as package:
                    package.writestr("plugin.json", '{"entry":"main.py"}')
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
        plugin_id = "desktop.lifecycle"

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

        first = run(
            {"action": "install", "path": str(EXAMPLE)},
            {"action": "enable", "plugin_id": plugin_id},
            {"action": "snapshot"},
        )
        self.assertTrue(first[-1]["plugins"][0]["loaded"])
        self.assertFalse(self.profile.joinpath("running").exists())
        self.assertFalse(run({"action": "snapshot"}, disabled=True)[0]["plugins"][0]["loaded"])
        self.assertTrue(run({"action": "snapshot"})[0]["plugins"][0]["loaded"])
        state = json.loads(self.profile.joinpath("state.json").read_text(encoding="utf-8"))
        self.assertEqual(state[plugin_id]["settings"]["load_count"], 2)
