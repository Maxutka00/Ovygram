"""Stage the pinned x64 interpreter, its link library and pybind11 headers.

Windows uses the official binaries. Linux has none, so CPython is built from the
pinned source, which requires a C toolchain and the development packages of the
libraries listed in REQUIRED_MODULES.
"""

import argparse
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import zipfile


PACKAGES = {
    "python-embed.zip": (
        "https://www.python.org/ftp/python/3.13.16/python-3.13.16-embeddable-amd64.zip",
        # Official Windows release manifest (windows-3.13.16.json).
        "589dc1e9d02549ca5f680710307ff9b77f6e3ffc4aa3efccd7fa54eeeafac94b",
    ),
    "python.nupkg": (
        "https://api.nuget.org/v3-flatcontainer/python/3.13.16/python.3.13.16.nupkg",
        "95fad176338f1d6a799e45946488063f4aa61764e6cff2f132ddeffbf7a04c34",
    ),
    "python-source.tar.xz": (
        "https://www.python.org/ftp/python/3.13.16/Python-3.13.16.tar.xz",
        # Digest from the release's Python-3.13.16.tar.xz.sigstore bundle.
        "f4b1bfb3c79b5bb11b8d228a12504163b4c0dab4d679828d8f5f26b6cb6ab35d",
    ),
    "pybind11.whl": (
        "https://files.pythonhosted.org/packages/88/c5/e98d9c51f3d5300d5e40ad9037dd6b3b60736fd02ab68dcc98c96be7592d/pybind11-3.0.2-py3-none-any.whl",
        "f8a6500548919cc33bcd220d5f984688326f574fa97f1107f2f4fdb4c6fb019f",
    ),
}
# configure silently skips modules whose libraries are missing.
REQUIRED_MODULES = "bz2,ctypes,hashlib,lzma,sqlite3,ssl,zlib"
STDLIB_EXCLUDED = (r"(^|/)(__pycache__|__phello__|config-3\.13-[^/]*|ensurepip|idlelib|"
                   r"lib-dynload|site-packages|test|tkinter|turtledemo)(/|$)")


def checked_download(downloads, name):
    url, digest = PACKAGES[name]
    path = downloads / name
    if not path.exists():
        temporary = path.with_suffix(".part")
        try:
            with urllib.request.urlopen(url, timeout=60) as response, temporary.open("wb") as output:
                shutil.copyfileobj(response, output)
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
    with path.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != digest:
            raise RuntimeError(f"SHA-256 mismatch: {path}")
    return path


def checked_archive(downloads, name):
    return zipfile.ZipFile(checked_download(downloads, name))


def prepare_windows(root, runtime, downloads):
    with checked_archive(downloads, "python-embed.zip") as archive:
        for name in archive.namelist():
            if "/" not in name and not name.endswith(("._pth", ".cat", ".json")):
                archive.extract(name, runtime)
    with checked_archive(downloads, "python.nupkg") as archive:
        for name in archive.namelist():
            if not name.endswith("/") and (
                name.startswith("tools/include/") or name == "tools/libs/python313.lib"
            ):
                archive.extract(name, root)


def write_stdlib_zip(stdlib, target):
    # Stored, not deflated: zlib is an extension module here, and it can't be
    # imported to read the archive the interpreter needs to start up.
    with zipfile.ZipFile(target, "w", zipfile.ZIP_STORED) as archive:
        for path in sorted(stdlib.rglob("*.pyc")):
            name = path.relative_to(stdlib).as_posix()
            if not re.search(STDLIB_EXCLUDED, name):
                archive.write(path, name)


def prepare_linux(root, runtime, downloads):
    source_archive = checked_download(downloads, "python-source.tar.xz")
    with tempfile.TemporaryDirectory(dir=downloads) as temporary:
        build = Path(temporary)
        with tarfile.open(source_archive) as archive:
            archive.extractall(build, filter="data")
        source = build / "Python-3.13.16"
        install = build / "install"
        subprocess.run([
            "./configure", f"--prefix={install}", "--enable-shared",
            "--without-ensurepip", "--disable-test-modules",
            # "$$" survives make; everything is relocated into one directory.
            # The argument replaces the caller's LDFLAGS, so they're kept here.
            "LDFLAGS=" + (os.environ.get("LDFLAGS", "") + r" -Wl,-rpath,\$$ORIGIN").strip(),
        ], cwd=source, check=True)
        subprocess.run(["make", f"-j{os.cpu_count()}"], cwd=source, check=True)
        subprocess.run(["make", "install"], cwd=source, check=True)

        stdlib = install / "lib/python3.13"
        shutil.copy2(install / "lib/libpython3.13.so.1.0", runtime)
        shutil.copy2(install / "bin/python3.13", runtime / "python")
        python = runtime / "python"
        subprocess.run([python, "-I", "-c", f"import {REQUIRED_MODULES}"],
                       env={"PYTHONHOME": str(install)}, check=True)
        subprocess.run([python, "-m", "compileall", "-q", "-b", "-x", STDLIB_EXCLUDED, stdlib],
                       env={"PYTHONHOME": str(install)}, check=True)
        write_stdlib_zip(stdlib, runtime / "python313.zip")
        for module in (stdlib / "lib-dynload").glob("*.so"):
            shutil.copy2(module, runtime)

        shutil.copytree(install / "include/python3.13", root / "tools/include",
                        dirs_exist_ok=True)
    libs = root / "tools/libs"
    libs.mkdir(parents=True, exist_ok=True)
    link = libs / "libpython3.13.so"
    link.unlink(missing_ok=True)
    link.symlink_to("../../python/libpython3.13.so.1.0")


def prepare(root, downloads, sdk, system_python=False):
    downloads.mkdir(parents=True, exist_ok=True)
    runtime = root / "python"
    runtime.mkdir(parents=True, exist_ok=True)
    if sys.platform == "linux":
        if not system_python:
            prepare_linux(root, runtime, downloads)
    elif system_python:
        raise RuntimeError("--system-python is supported only on Linux.")
    elif sys.platform == "win32":
        prepare_windows(root, runtime, downloads)
    else:
        raise RuntimeError(f"Unsupported platform: {sys.platform}")
    with checked_archive(downloads, "pybind11.whl") as archive:
        for name in archive.namelist():
            if not name.endswith("/") and name.startswith("pybind11/include/"):
                archive.extract(name, root)
        license_name = "pybind11-3.0.2.dist-info/licenses/LICENSE"
        (runtime / "pybind11-LICENSE.txt").write_bytes(archive.read(license_name))
    shutil.copytree(sdk, runtime / "sdk", dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    interpreter = "System Python mode:" if system_python else "CPython 3.13.16 and"
    print(f"{interpreter} pybind11 3.0.2 staged at {root}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--downloads", required=True, type=Path)
    parser.add_argument("--sdk", required=True, type=Path)
    parser.add_argument("--system-python", action="store_true",
                        help="stage only pybind11 and the SDK for OVYGRAM_SYSTEM_PYTHON")
    args = parser.parse_args()
    prepare(args.root.resolve(), args.downloads.resolve(), args.sdk.resolve(),
            args.system_python)
