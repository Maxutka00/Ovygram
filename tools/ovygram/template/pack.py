"""Packs the plugin into dist/<id>.ovyzip for «Импортировать плагин» and for
the review bot, which needs the file named by the plugin ID.

Run from this directory: python pack.py
"""

import ast
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
SKIPPED = {"pack.py", "pyrightconfig.json", "README.md", "dist", "__pycache__", ".vscode", ".idea"}


def metadata(entry):
    values = {}
    for node in ast.parse(entry.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__id__":
                    values[target.id] = ast.literal_eval(node.value)
    return values["__id__"].lower()


def main():
    entry = ROOT / json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))["entry"]
    identity = metadata(entry)
    target = ROOT / "dist" / f"{identity}.ovyzip"
    target.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(ROOT.rglob("*")):
            relative = path.relative_to(ROOT)
            if path.is_file() and not SKIPPED.intersection(relative.parts):
                archive.write(path, relative.as_posix())
    print(target)


if __name__ == "__main__":
    main()
