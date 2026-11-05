"""Stage the pinned Windows x64 interpreter, import library and pybind11 headers."""

import argparse
import hashlib
from pathlib import Path
import shutil
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
    "pybind11.whl": (
        "https://files.pythonhosted.org/packages/88/c5/e98d9c51f3d5300d5e40ad9037dd6b3b60736fd02ab68dcc98c96be7592d/pybind11-3.0.2-py3-none-any.whl",
        "f8a6500548919cc33bcd220d5f984688326f574fa97f1107f2f4fdb4c6fb019f",
    ),
}

def checked_archive(downloads, name):
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
    return zipfile.ZipFile(path)


def prepare(root, downloads, sdk):
    downloads.mkdir(parents=True, exist_ok=True)
    runtime = root / "python"
    runtime.mkdir(parents=True, exist_ok=True)
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
    with checked_archive(downloads, "pybind11.whl") as archive:
        for name in archive.namelist():
            if not name.endswith("/") and name.startswith("pybind11/include/"):
                archive.extract(name, root)
        license_name = "pybind11-3.0.2.dist-info/licenses/LICENSE"
        (runtime / "pybind11-LICENSE.txt").write_bytes(archive.read(license_name))
    shutil.copytree(sdk, runtime / "sdk", dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    print(f"CPython 3.13.16 and pybind11 3.0.2 staged at {root}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--downloads", required=True, type=Path)
    parser.add_argument("--sdk", required=True, type=Path)
    args = parser.parse_args()
    prepare(args.root.resolve(), args.downloads.resolve(), args.sdk.resolve())
