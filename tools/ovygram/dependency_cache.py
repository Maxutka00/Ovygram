import json
import os
from pathlib import Path, PurePosixPath
import shutil
import zipfile


GROUPS = ('foundation', 'qt', 'extras')
EXTRAS = {'tg_owt', 'ada', 'tde2e', 'tlottie', 'wallet-engine', 'tdesktop_rust'}
MAX_ARCHIVE = 5 * 1024 ** 3 // 2


def group_for(name):
    if name.startswith('qt_6.') or name.startswith('Qt-6.'):
        return 'qt'
    return 'extras' if name in EXTRAS else 'foundation'


def selected_roots(root, group):
    if group not in GROUPS:
        raise ValueError('Unknown dependency group.')
    libraries = root / 'TBuild/Libraries/win64'
    paths = []
    if group == 'foundation':
        paths.append(root / 'TBuild/ThirdParty')
    if libraries.exists():
        for child in libraries.iterdir():
            if child.name == 'cache_keys':
                paths.extend(key for key in child.iterdir() if group_for(key.name) == group)
            elif child.name == 'local':
                if group in ('foundation', 'extras'):
                    paths.append(child)
            elif group_for(child.name) == group:
                paths.append(child)
    return paths


def keep_file(path):
    parts = path.parts
    if '.git' in parts or '__pycache__' in parts:
        return False
    if ('var', 'cache') in zip(parts, parts[1:]):
        return False
    if ('registry', 'cache') in zip(parts, parts[1:]):
        return False
    if path.suffix.lower() in {'.obj', '.o'}:
        return any(part.startswith('objects-') for part in parts)
    return path.suffix.lower() not in {'.pdb', '.pch', '.ipch', '.ilk', '.idb', '.tlog'}


def files_under(paths):
    for path in paths:
        if path.is_file():
            yield path
        elif path.is_dir():
            for directory, subdirs, files in os.walk(path, followlinks=False):
                subdirs[:] = [name for name in subdirs
                              if name not in ('.git', '__pycache__')
                              and not (Path(directory) / name).is_symlink()]
                for name in files:
                    file = Path(directory) / name
                    if not file.is_symlink() and keep_file(file):
                        yield file


def pack(root, group, identity, maximum=MAX_ARCHIVE):
    target = root / 'dependency-cache' / group
    target.mkdir(parents=True, exist_ok=True)
    archive = target / 'dependencies.zip'
    partial = target / 'dependencies.tmp'
    count = 0
    try:
        with zipfile.ZipFile(partial, 'w', zipfile.ZIP_DEFLATED, compresslevel=3) as output:
            output.writestr('manifest.json', json.dumps({
                'group': group, 'identity': identity, 'format': 2}))
            for path in files_under(selected_roots(root, group)):
                output.write(path, path.relative_to(root).as_posix())
                count += 1
                if output.fp.tell() > maximum:
                    break
        size = partial.stat().st_size
        if size > maximum or count == 0:
            partial.unlink()
            return {'save': False, 'bytes': size, 'files': count,
                    'reason': 'empty or exceeds compressed archive limit'}
        partial.replace(archive)
        return {'save': True, 'bytes': size, 'files': count}
    except BaseException:
        partial.unlink(missing_ok=True)
        raise


def restore(root, group, identity):
    archive = root / 'dependency-cache' / group / 'dependencies.zip'
    if not archive.exists():
        return False
    with zipfile.ZipFile(archive) as source:
        manifest = json.loads(source.read('manifest.json'))
        if manifest != {'group': group, 'identity': identity, 'format': 2}:
            raise RuntimeError('Dependency snapshot does not match this build.')
        entries = [entry for entry in source.infolist() if entry.filename != 'manifest.json']
        for entry in entries:
            name = PurePosixPath(entry.filename)
            if ('..' in name.parts or name.is_absolute() or '\\' in entry.filename
                    or ':' in entry.filename or entry.is_dir()
                    or not (entry.filename.startswith('TBuild/ThirdParty/')
                            or entry.filename.startswith('TBuild/Libraries/win64/'))):
                raise RuntimeError('Unexpected path in dependency snapshot.')
        for entry in entries:
            if shutil.disk_usage(root).free < entry.file_size + 2 * 1024 ** 3:
                raise RuntimeError('Insufficient disk reserve to restore dependencies.')
            destination = root.joinpath(*PurePosixPath(entry.filename).parts)
            if not destination.resolve().is_relative_to(root.resolve()):
                raise RuntimeError('Dependency snapshot escapes build root.')
            destination.parent.mkdir(parents=True, exist_ok=True)
            with source.open(entry) as reader, destination.open('wb') as writer:
                shutil.copyfileobj(reader, writer)
    return True
