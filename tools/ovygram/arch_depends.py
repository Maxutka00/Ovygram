"""Prints the Arch Linux packages a Linux build needs, for the PKGBUILD.

Reads the libraries the binary and the plugin runtime link directly
(DT_NEEDED) and asks pacman which package owns each one. Run on the Arch
machine that made the build:

    python tools/ovygram/arch_depends.py out/Release
"""

from pathlib import Path
import re
import subprocess
import sys

# Always present on Arch, not listed by convention.
IMPLIED = {"glibc", "gcc-libs"}


def needed(path):
    output = subprocess.run(["readelf", "-d", str(path)], check=True,
                            capture_output=True, text=True).stdout
    return re.findall(r"\(NEEDED\)\s+Shared library: \[([^\]]+)\]", output)


def resolve(library, search):
    for directory in search:
        candidate = Path(directory) / library
        if candidate.exists():
            return candidate
    return None


def owner(path):
    result = subprocess.run(["pacman", "-Qoq", str(path)], capture_output=True, text=True)
    return result.stdout.strip() or None


def main():
    build = Path(sys.argv[1] if len(sys.argv) > 1 else "out/Release").resolve()
    python = build / "python"
    elves = [build / "Ovygram", *sorted(python.glob("*.so")), *sorted(python.glob("*.so.*"))]
    bundled = {path.name for path in elves}
    search = ["/usr/lib", "/usr/lib64", "/lib"]
    packages, unknown = set(), set()
    for elf in elves:
        for library in needed(elf):
            if library in bundled:
                continue  # libpython and the host come with Ovygram.
            path = resolve(library, search)
            package = owner(path) if path else None
            if package:
                packages.add(package)
            else:
                unknown.add(library)
    packages -= IMPLIED
    print("depends=(" + "\n         ".join(f"'{name}'" for name in sorted(packages)) + ")")
    if unknown:
        print("# Not found:", " ".join(sorted(unknown)), file=sys.stderr)


if __name__ == "__main__":
    main()
