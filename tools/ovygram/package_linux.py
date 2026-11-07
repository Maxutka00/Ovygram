"""Packs a Linux build into ovygram-<version>-linux-x86_64.tar.xz.

The archive holds the Ovygram binary, the python directory next to it
(the plugin runtime looks for it there), the .desktop file and icons named
by the application ID, and the license. The binary is linked against the
system libraries of the build machine, see packaging/arch for the package.

    python tools/ovygram/package_linux.py --build out/Release --output dist
"""

import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from baseline import CLIENT_VERSION, OVYGRAM_VERSION  # noqa: E402

APP_ID = "io.github.maxutka00.Ovygram"
ICON_SIZES = (16, 32, 48, 64, 128, 256, 512)
# A stale python directory would ship without dependency support.
REQUIRED_RUNTIME = ("ovygram_host.so", "python313.zip", "pip.whl",
                    "sdk/ovygram_runtime.py", "sdk/ovygram_deps.py")


def check_build(build):
    binary = build / "Ovygram"
    if not binary.is_file():
        raise SystemExit(f"No Ovygram binary in {build}.")
    python = build / "python"
    missing = [name for name in REQUIRED_RUNTIME if not (python / name).exists()]
    if missing:
        raise SystemExit("The python directory is incomplete: " + ", ".join(missing))
    return binary, python


def stage(build, target, strip):
    binary, python = check_build(build)
    target.mkdir(parents=True)
    shutil.copy2(binary, target / "Ovygram")
    if strip:
        subprocess.run(["strip", "--strip-unneeded", str(target / "Ovygram")], check=True)
    shutil.copytree(python, target / "python",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copy2(ROOT / "packaging/linux" / f"{APP_ID}.desktop", target / f"{APP_ID}.desktop")
    for size in ICON_SIZES:
        icon = target / "icons/hicolor" / f"{size}x{size}" / "apps" / f"{APP_ID}.png"
        icon.parent.mkdir(parents=True)
        shutil.copy2(ROOT / "Telegram/Resources/art" / f"icon{size}.png", icon)
    shutil.copy2(ROOT / "LICENSE", target / "LICENSE")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", required=True, type=Path, help="directory with the Ovygram binary")
    parser.add_argument("--output", default=ROOT / "dist", type=Path)
    parser.add_argument("--no-strip", action="store_true", help="keep debug symbols")
    args = parser.parse_args()
    version = f"{OVYGRAM_VERSION}-{CLIENT_VERSION}"
    name = f"ovygram-{version}-linux-x86_64"
    args.output.mkdir(parents=True, exist_ok=True)
    archive = args.output / f"{name}.tar.xz"
    with tempfile.TemporaryDirectory() as temporary:
        staged = Path(temporary) / name
        stage(args.build.resolve(), staged, not args.no_strip)
        with tarfile.open(archive, "w:xz", preset=6) as tar:
            tar.add(staged, arcname=name)
    with archive.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    archive.with_name(archive.name + ".sha256").write_text(f"{digest}  {archive.name}\n")
    print(f"{archive}\n{digest}")


if __name__ == "__main__":
    main()
