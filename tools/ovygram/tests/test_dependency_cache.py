import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).parents[1]))
import dependency_cache as cache
from prepare_group import grouped_recipe


class CacheTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def make(self, name, data=b'file'):
        path = self.root / 'TBuild/Libraries/win64' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def test_cache_keeps_generated_objects_and_rust_sources(self):
        for name in ('wallet-engine/src/lib.rs', 'tlottie/Cargo.toml',
                     'Qt-6.11.2/lib/objects-Debug/Plugin/init.obj'):
            self.assertTrue(cache.keep_file(Path(name)))
        for name in ('qt_6.11.2/.git/objects/data', 'zlib/Debug/code.obj',
                     'Qt-6.11.2/lib/code.pdb'):
            self.assertFalse(cache.keep_file(Path(name)))

    def test_roundtrip_selects_only_its_group(self):
        library = self.make('zlib/Debug/zlib.lib')
        rust = self.make('wallet-engine/src/lib.rs')
        qt = self.make('Qt-6.11.2/lib/Qt6Core.lib')
        self.make('zlib/Debug/code.obj')
        self.make('cache_keys/zlib')
        self.assertTrue(cache.pack(self.root, 'foundation', 'identity')['save'])
        library.unlink()
        self.assertTrue(cache.restore(self.root, 'foundation', 'identity'))
        self.assertEqual(library.read_bytes(), b'file')
        archive = self.root / 'dependency-cache/foundation/dependencies.zip'
        with zipfile.ZipFile(archive) as source:
            names = source.namelist()
        self.assertNotIn(rust.relative_to(self.root).as_posix(), names)
        self.assertNotIn(qt.relative_to(self.root).as_posix(), names)
        self.assertFalse(any(name.endswith('.obj') for name in names))

    def test_identity_mismatch_is_rejected(self):
        self.make('zlib/Debug/zlib.lib')
        cache.pack(self.root, 'foundation', 'first')
        with self.assertRaisesRegex(RuntimeError, 'does not match'):
            cache.restore(self.root, 'foundation', 'second')

    def test_budget_uses_compressed_size(self):
        self.make('zlib/Debug/zlib.lib', bytes(64 * 1024))
        result = cache.pack(self.root, 'foundation', 'identity', maximum=1024)
        self.assertTrue(result['save'])
        self.assertLess(result['bytes'], 1024)

    def test_oversize_snapshot_not_saved(self):
        self.make('zlib/Debug/zlib.lib', os.urandom(8192))
        self.assertFalse(cache.pack(self.root, 'foundation', 'id', maximum=1024)['save'])
        self.assertFalse((self.root / 'dependency-cache/foundation/dependencies.zip').exists())

    def test_traversal_rejected_before_any_file_is_restored(self):
        archive = self.root / 'dependency-cache/foundation/dependencies.zip'
        archive.parent.mkdir(parents=True)
        with zipfile.ZipFile(archive, 'w') as source:
            source.writestr('manifest.json', json.dumps({
                'group': 'foundation', 'identity': 'id', 'format': 2}))
            source.writestr('TBuild/ThirdParty/good.txt', 'good')
            source.writestr('TBuild/ThirdParty/../../escape', 'bad')
        with self.assertRaisesRegex(RuntimeError, 'Unexpected path'):
            cache.restore(self.root, 'foundation', 'id')
        self.assertFalse((self.root / 'TBuild/ThirdParty/good.txt').exists())

    def test_recipe_filter_preserves_original_skip_logic(self):
        recipe = '''
stages = [{'name': 'zlib', 'valid': True}, {'name': 'qt_6.11.2', 'valid': False},
          {'name': 'tg_owt', 'valid': False}]
built = []
def runStages():
    for entry in stages:
        if not entry['valid']:
            built.append(entry['name'])
runStages()
'''
        for group, expected in [('foundation', []), ('qt', ['qt_6.11.2']),
                                ('extras', ['tg_owt'])]:
            scope = {'_desktop_group_for': cache.group_for}
            exec(grouped_recipe(recipe, 'fixture.py', group), scope)
            self.assertEqual(scope['built'], expected)


if __name__ == '__main__':
    unittest.main()
