import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import zipfile


sys.path.insert(0, str(Path(__file__).parents[1]))
import dependency_cache


spec = importlib.util.spec_from_file_location(
    'baseline', Path(__file__).parents[1] / 'baseline.py')
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)


class BaselineTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_success_records_output(self):
        log = self.root / 'test.log'
        result = baseline.run_monitored(
            [sys.executable, '-c', 'print("built")'], self.root, log,
            time.time() + 10, minimum_free=0, poll_seconds=0.02)
        self.assertEqual(result['status'], 'success')
        self.assertIn('built', log.read_text())

    def test_command_failure_is_not_success(self):
        with self.assertRaisesRegex(RuntimeError, 'code 7'):
            baseline.run_monitored(
                [sys.executable, '-c', 'raise SystemExit(7)'], self.root,
                self.root / 'test.log', time.time() + 10,
                minimum_free=0, poll_seconds=0.02)

    def test_timeout_terminates_process(self):
        with self.assertRaisesRegex(RuntimeError, 'allowance exhausted'):
            baseline.run_monitored(
                [sys.executable, '-c', 'import time; time.sleep(30)'],
                self.root, self.root / 'test.log', time.time() + 0.2,
                minimum_free=0, poll_seconds=0.02)

    def test_disk_preflight_does_not_start_command(self):
        with patch.object(subprocess, 'Popen') as start:
            with self.assertRaisesRegex(RuntimeError, 'Insufficient disk'):
                baseline.run_monitored([], self.root, self.root / 'test.log',
                                       time.time() + 10, minimum_free=10 ** 30)
            start.assert_not_called()

    def test_package_requires_real_binary(self):
        with self.assertRaisesRegex(RuntimeError, 'No compiled'):
            baseline.package(self.root, self.root / 'artifacts')

    def test_package_excludes_account_data(self):
        directory = self.root / 'out/Debug'
        directory.mkdir(parents=True)
        (directory / 'Telegram.exe').write_bytes(b'test binary fixture')
        (directory / 'secret.session').write_text('must not be shipped')
        archive = baseline.package(self.root, self.root / 'artifacts')
        with zipfile.ZipFile(archive) as source:
            self.assertEqual(set(source.namelist()), {
                'Telegram.exe', 'TelegramForcePortable', 'BASELINE.txt'})

    def test_versions_match_client_source(self):
        source = (Path(__file__).parents[3] / 'Telegram/SourceFiles/core/version.h').read_text(
            encoding='utf-8')
        self.assertIn(f'AppVersionStr = "{baseline.CLIENT_VERSION}";', source)
        self.assertIn(f'OvygramVersionStr = "{baseline.OVYGRAM_VERSION}";', source)

    def test_plugin_package_uses_release_outputs(self):
        debug = self.root / 'out/Debug'
        debug.mkdir(parents=True)
        (debug / 'Ovygram.exe').write_bytes(b'debug executable')
        release = self.root / 'out/Release'
        runtime = release / 'python'
        runtime.mkdir(parents=True)
        (release / 'Ovygram.exe').write_bytes(b'release executable')
        (runtime / 'ovygram_host.dll').write_bytes(b'release host')
        archive = baseline.package(self.root, self.root / 'artifacts', True, 'Release')
        self.assertEqual(archive.name, 'ovygram-0.1.0-7.4.3-win64-release.zip')
        with zipfile.ZipFile(archive) as source:
            self.assertEqual(source.read('Ovygram.exe'), b'release executable')
            self.assertEqual(source.read('python/ovygram_host.dll'), b'release host')

    def test_cache_identity_changes_with_compiler_and_recipe(self):
        recipe = self.root / 'Telegram/build/prepare/prepare.py'
        recipe.parent.mkdir(parents=True)
        recipe.write_text('recipe one')
        toolchain = dict(image_version='image', msvc='14.44', sdk='26100',
                         python_version='3.12')
        first = baseline.cache_identity(self.root, toolchain)
        toolchain['msvc'] = '14.45'
        self.assertNotEqual(first, baseline.cache_identity(self.root, toolchain))
        toolchain['msvc'] = '14.44'
        recipe.write_text('recipe two')
        self.assertNotEqual(first, baseline.cache_identity(self.root, toolchain))

    def test_cache_size_handles_missing_paths(self):
        (self.root / 'one').write_bytes(b'123')
        (self.root / 'nested').mkdir()
        (self.root / 'nested/two').write_bytes(b'4567')
        self.assertEqual(baseline.cache_size([
            self.root, self.root / 'missing']), 7)

    def dependency_cache_fixture(self):
        source = self.root / 'TBuild/tdesktop'
        recipe = source / 'Telegram/build/prepare/prepare.py'
        recipe.parent.mkdir(parents=True)
        recipe.write_text('pinned recipe')
        toolchain = dict(image='fixture', image_version='image', msvc='14.44',
                         sdk='26100', python_version='3.12')
        baseline.write_json(self.root / 'reports/toolchain.json', toolchain)
        baseline.write_json(self.root / 'reports/baseline.json',
                            {'configuration': 'Release'})
        return baseline.cache_identity(source, toolchain)

    def restore_dependencies(self, key='', required=True):
        arguments = ['baseline.py', 'cache-restore', '--root', str(self.root),
                     '--group', 'foundation']
        if required:
            arguments.append('--require-cache')
        with patch.object(sys, 'argv', arguments), patch.dict(
                baseline.os.environ, {'RESTORED_CACHE_KEY': key}):
            baseline.main()

    def test_required_dependency_cache_stops_on_cache_miss(self):
        self.dependency_cache_fixture()
        with self.assertRaisesRegex(RuntimeError, 'No compatible dependency cache'):
            self.restore_dependencies()
        self.assertFalse((self.root / 'TBuild/ThirdParty').exists())

    def test_required_release_cache_rejects_debug_before_unpacking(self):
        debug_identity = self.dependency_cache_fixture()
        with patch.object(dependency_cache, 'restore') as restore:
            with self.assertRaisesRegex(RuntimeError, 'Release dependency cache is required'):
                self.restore_dependencies(f'{debug_identity}-foundation')
            restore.assert_not_called()

    def test_required_dependency_cache_restores_saved_release_files(self):
        identity = baseline.release_cache_identity(self.dependency_cache_fixture())
        library = self.root / 'TBuild/Libraries/win64/zlib/Release/zlib.lib'
        library.parent.mkdir(parents=True)
        library.write_bytes(b'release library fixture')
        self.assertTrue(dependency_cache.pack(self.root, 'foundation', identity)['save'])
        library.unlink()
        self.restore_dependencies(f'{identity}-foundation')
        self.assertEqual(library.read_bytes(), b'release library fixture')

    def test_optional_dependency_cache_allows_initial_preparation(self):
        self.dependency_cache_fixture()
        self.restore_dependencies(required=False)


if __name__ == '__main__':
    unittest.main()
