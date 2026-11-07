import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import zipfile


UPSTREAM = '3a2a9a34e833d3243a13787215b8a7cdcf5dc3c3'
CLIENT_VERSION = '7.3.5'
# Keep in sync with OvygramVersionStr in Telegram/SourceFiles/core/version.h.
OVYGRAM_VERSION = '0.1.0'
GIB = 1024 ** 3


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2), encoding='utf-8')
    temporary.replace(path)


def git(source, *arguments):
    return subprocess.check_output(
        ['git', '-C', str(source), *arguments], text=True).strip()


def verify_source(source, expected=UPSTREAM):
    if git(source, 'rev-parse', 'HEAD') != expected:
        raise RuntimeError('Source does not match the expected commit.')
    modules = git(source, 'submodule', 'status', '--recursive').splitlines()
    if any(line and line[0] in '-+U' for line in modules):
        raise RuntimeError('Submodule missing or not at its pinned revision.')
    if git(source, 'status', '--porcelain', '--untracked-files=no'):
        raise RuntimeError('Baseline source has tracked modifications.')
    return modules


def stop_process(process):
    if process.poll() is not None:
        return
    if os.name == 'nt':
        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       check=False)
    else:
        process.kill()
    process.wait(timeout=20)


def run_monitored(command, cwd, log, deadline, minimum_free=2 * GIB,
                  poll_seconds=2):
    started = time.time()
    result = {'command': command, 'started': started, 'status': 'running'}
    free = shutil.disk_usage(cwd).free
    result['minimum_free_bytes'] = free
    if free < minimum_free:
        raise RuntimeError(f'Insufficient disk: {free / GIB:.2f} GiB free.')
    if time.time() >= deadline:
        raise RuntimeError('Build time allowance exhausted before starting.')
    process = None
    log.parent.mkdir(parents=True, exist_ok=True)
    try:
        with log.open('wb') as stream:
            process = subprocess.Popen(command, cwd=cwd, stdout=stream,
                                       stderr=subprocess.STDOUT)
            heartbeat = 0
            while process.poll() is None:
                free = shutil.disk_usage(cwd).free
                result['minimum_free_bytes'] = min(
                    free, result['minimum_free_bytes'])
                if free < minimum_free:
                    raise RuntimeError(f'Disk reserve reached: {free / GIB:.2f} GiB.')
                if time.time() >= deadline:
                    raise RuntimeError('Build time allowance exhausted.')
                if time.monotonic() >= heartbeat:
                    print(f'Running {command[0]}; free {free / GIB:.2f} GiB', flush=True)
                    heartbeat = time.monotonic() + 45
                time.sleep(poll_seconds)
            result['returncode'] = process.returncode
            if process.returncode:
                raise RuntimeError(f'Command failed with code {process.returncode}; see {log.name}.')
        result['status'] = 'success'
    except BaseException as error:
        result['status'] = 'failed'
        result['error'] = str(error)
        if log.exists():
            with log.open('rb') as stream:
                stream.seek(max(0, log.stat().st_size - 8000))
                print(stream.read().decode('utf-8', errors='replace'), flush=True)
        raise
    finally:
        if process is not None:
            stop_process(process)
        result['seconds'] = round(time.time() - started, 2)
        write_json(log.with_suffix('.json'), result)
    return result


def package(source, target, plugins=False, configuration='Debug'):
    binary_name = 'Ovygram.exe' if plugins else 'Telegram.exe'
    executable = source / 'out' / configuration / binary_name
    if not executable.is_file():
        raise RuntimeError('No compiled client executable; refusing to package.')
    target.mkdir(parents=True, exist_ok=True)
    name = 'ovygram' if plugins else 'upstream-baseline'
    version = f'{OVYGRAM_VERSION}-{CLIENT_VERSION}' if plugins else CLIENT_VERSION
    archive = target / f'{name}-{version}-win64-{configuration.lower()}.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as output:
        output.write(executable, binary_name)
        output.writestr('TelegramForcePortable', '')
        if plugins:
            binary_dir = executable.parent
            runtime = binary_dir / 'python'
            if not (runtime / 'ovygram_host.dll').is_file():
                raise RuntimeError('Python host DLL is missing from the package directory.')
            for path in sorted(runtime.rglob('*')):
                if path.is_file():
                    output.write(path, path.relative_to(binary_dir).as_posix())
            if (binary_dir / 'd3dcompiler_47.dll').is_file():
                output.write(binary_dir / 'd3dcompiler_47.dll', 'd3dcompiler_47.dll')
            output.writestr('README.txt',
                            f'Ovygram {configuration} build. Test API credentials.\n')
        else:
            output.writestr('BASELINE.txt',
                            'Unmodified upstream source. Test API credentials. '
                            'No Python plugins yet. Not a production release.\n')
    with archive.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    archive.with_suffix('.zip.sha256').write_text(
        f'{digest}  {archive.name}\n', encoding='utf-8')
    return archive


def cache_identity(source, toolchain):
    inputs = {key: toolchain[key] for key in (
        'image_version', 'msvc', 'sdk', 'python_version')}
    inputs['source'] = UPSTREAM
    inputs['recipe'] = hashlib.sha256(
        (source / 'Telegram/build/prepare/prepare.py').read_bytes()).hexdigest()
    inputs['build_root'] = str(source.parent.resolve()).lower()
    inputs['cache_implementation'] = hashlib.sha256(
        Path(__file__).with_name('dependency_cache.py').read_bytes()
        + Path(__file__).with_name('prepare_group.py').read_bytes()).hexdigest()
    digest = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()
    return f'pd-win64-qt6-debug-v2-{digest}'


def release_cache_identity(debug_identity):
    release_script = Path(__file__).with_name('prepare_release_group.py')
    digest = hashlib.sha256(debug_identity.encode() + release_script.read_bytes()).hexdigest()
    return f'pd-win64-qt6-release-v1-{digest}'


def cache_size(paths):
    total = 0
    for path in paths:
        if not path.exists():
            continue
        for directory, _, files in os.walk(path, followlinks=False):
            for name in files:
                file = Path(directory) / name
                if file.is_symlink():
                    continue
                total += file.stat().st_size
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=[
        'init', 'verify', 'cache-key', 'cache-pack', 'cache-restore',
        'prepare-foundation', 'prepare-qt', 'prepare-extras',
        'configure', 'verify-integration', 'build', 'package', 'report'])
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--mode', choices=['inspect', 'build', 'plugin-smoke', 'plugins'], default='inspect')
    parser.add_argument('--group', choices=['foundation', 'qt', 'extras'])
    parser.add_argument('--require-cache', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    source = root / 'TBuild/tdesktop'
    reports = root / 'reports'
    state_path = reports / 'baseline.json'
    if args.action == 'init':
        write_json(state_path, {
            'upstream': UPSTREAM, 'mode': args.mode, 'started': time.time(),
            'deadline': time.time() + 345 * 60,
            'initial_free_bytes': shutil.disk_usage(root).free,
            'status': 'initialized', 'stage': 'preflight',
            'configuration': 'Release' if args.mode == 'plugins' else 'Debug',
            'plugins_implemented': args.mode == 'plugins',
        })
        return
    state = json.loads(state_path.read_text(encoding='utf-8'))
    if args.action in ('cache-key', 'cache-pack', 'cache-restore'):
        import dependency_cache
        toolchain = json.loads((reports / 'toolchain.json').read_text(encoding='utf-8-sig'))
        debug_identity = cache_identity(source, toolchain)
        identity = debug_identity
        release_fallback = ''
        if state['configuration'] == 'Release':
            identity = release_cache_identity(debug_identity)
            # These two images provide the same pinned Windows toolchain.
            compatible_images = ('20261030.294.1', '20261103.298.1')
            if (toolchain['image'] == 'win25-vs2026'
                    and toolchain['image_version'] in compatible_images
                    and toolchain['msvc'] == '14.44.35207'
                    and toolchain['sdk'].rstrip('\\') == '10.0.26100.0'
                    and toolchain['python_version'] == 'Python 3.12.10'
                    and toolchain['cmake_version'] == 'cmake version 4.4.5'):
                other = next(image for image in compatible_images
                             if image != toolchain['image_version'])
                release_fallback = release_cache_identity(
                    cache_identity(source, {**toolchain, 'image_version': other}))
        if args.action == 'cache-restore':
            if not args.group:
                parser.error('--group required')
            restored_key = os.getenv('RESTORED_CACHE_KEY', '')
            if restored_key == f'{debug_identity}-{args.group}':
                if args.require_cache and state['configuration'] == 'Release':
                    raise RuntimeError(
                        f'A Release dependency cache is required for {args.group}; '
                        'the restored Debug snapshot would require rebuilding. '
                        'Prepare Release dependencies separately, then retry on the same branch.')
                identity = debug_identity
            elif release_fallback and restored_key == f'{release_fallback}-{args.group}':
                identity = release_fallback
            elif restored_key and restored_key != f'{identity}-{args.group}':
                raise RuntimeError('Unexpected dependency cache key.')
            restored = dependency_cache.restore(root, args.group, identity)
            if args.require_cache and not restored:
                raise RuntimeError(
                    f'No compatible dependency cache for {args.group}. '
                    'Stopping before dependency preparation to preserve the build time allowance. '
                    'Prepare dependencies separately, then retry on the same branch.')
            print('Snapshot restored:', restored)
            return
        elif args.action == 'cache-key':
            value = (f'key={identity}\ndebug-key={debug_identity}\n'
                     f'release-fallback-key={release_fallback}')
        else:
            if not args.group:
                parser.error('--group required')
            result = dependency_cache.pack(root, args.group, identity)
            write_json(reports / f'cache-{args.group}.json', result)
            value = f"save={str(result['save']).lower()}"
        print(value)
        if os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as stream:
                stream.write(value + '\n')
        return
    if args.action == 'report':
        state['job_result'] = os.environ.get('JOB_RESULT', 'unknown')
        state['elapsed_seconds'] = round(time.time() - state['started'], 2)
        state['final_free_bytes'] = shutil.disk_usage(root).free
        toolchain_path = reports / 'toolchain.json'
        if toolchain_path.exists():
            state['toolchain'] = json.loads(toolchain_path.read_text(encoding='utf-8-sig'))
        if state['mode'] == 'inspect':
            state['status'] = ('inspected' if state['toolchain']['status'] == 'ready'
                               else 'blocked') if 'toolchain' in state else 'blocked'
        write_json(state_path, state)
        summary = ('# Upstream baseline\n\n'
                   f"Mode: {state['mode']}\n\n"
                   f"Configuration: {state['configuration']}\n\n"
                   f"Status: {state['status']}\n\n"
                   f"Last stage: {state['stage']}\n\n"
                   f"Elapsed: {state['elapsed_seconds']} seconds\n\n"
                   f"Free disk: {state['final_free_bytes'] / GIB:.2f} GiB\n\n"
                   'A successful inspect run is not a compiled client.\n')
        reports.joinpath('SUMMARY.md').write_text(summary, encoding='utf-8')
        if os.environ.get('GITHUB_STEP_SUMMARY'):
            with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as stream:
                stream.write(summary)
        print(summary)
        return
    plugin_mode = state['mode'] in ('plugin-smoke', 'plugins')
    configuration = state['configuration']
    state['stage'] = args.action
    write_json(state_path, state)
    try:
        if args.action == 'verify':
            expected = os.environ['GITHUB_SHA'] if plugin_mode else UPSTREAM
            state['source_commit'] = expected
            state['submodules'] = verify_source(source, expected)
            free = shutil.disk_usage(root).free
            if free < 20 * GIB:
                raise RuntimeError(f'Need 20 GiB initial reserve; available {free / GIB:.2f} GiB.')
        elif args.action == 'package':
            state['archive'] = str(package(source, root / 'artifacts', plugin_mode, configuration))
            state['status'] = 'compiled'
        else:
            commands = {
                'configure': [sys.executable, str(source / 'Telegram/configure.py'),
                              '-G', 'Ninja Multi-Config',
                              '-D', 'TDESKTOP_API_TEST=ON',
                              '-D', f'CMAKE_CONFIGURATION_TYPES={configuration}',
                              '-D', 'CMAKE_MSVC_DEBUG_INFORMATION_FORMAT=',
                              '-D', 'DESKTOP_APP_DISABLE_AUTOUPDATE=ON',
                              '-D', 'DESKTOP_APP_DISABLE_CRASH_REPORTS=ON'],
                'build': ['cmake', '--build', str(source / 'out'),
                          '--config', configuration, '--target', 'Telegram', '--parallel', '2'],
                'verify-integration': [
                    'cmake', '--build', str(source / 'out'), '--config', configuration,
                    '--parallel', '2', '--target', *(
                        f'Telegram/CMakeFiles/Telegram.dir/{configuration}/SourceFiles/' + unit + '.cpp.obj'
                        for unit in (
                            'core/plugin_runtime_bridge', 'core/application', 'core/launcher',
                            'settings/sections/settings_main', 'settings/sections/settings_plugins',
                            'api/api_plugins', 'api/api_updates', 'mtproto/mtp_instance',
                            'window/window_session_controller',
                        )
                    ),
                ],
            }
            if args.action.startswith('prepare-'):
                script = ('prepare_release_group.py' if configuration == 'Release'
                          else 'prepare_group.py')
                commands[args.action] = [sys.executable,
                    str(Path(__file__).with_name(script)),
                    args.action.removeprefix('prepare-'),
                    str(source / 'Telegram/build/prepare/prepare.py')]
            if args.action == 'configure' and plugin_mode:
                commands['configure'].extend(['-D', f'OVYGRAM_PYTHON_ROOT={root / "plugin-python"}'])
                # Limit optimizer work in the C++ client on the two-core
                # runner. Prepared Qt and media libraries keep their flags.
                commands['configure'].extend([
                    '-D', 'CMAKE_CXX_FLAGS_RELEASE:STRING=/O1 /Ob1 /DNDEBUG',
                ])
            run_monitored(commands[args.action], source / 'Telegram',
                          reports / f'{args.action}.log', state['deadline'])
    except Exception as error:
        state['status'] = 'blocked'
        state['error'] = str(error)
        raise
    finally:
        write_json(state_path, state)


if __name__ == '__main__':
    main()
