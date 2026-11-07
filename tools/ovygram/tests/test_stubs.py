"""The hand-written .pyi files must match the modules they describe."""

import ast
from pathlib import Path
import unittest

SDK = Path(__file__).resolve().parents[3] / "Telegram/PluginSDK"
STUBS = ("desktop/ui", "desktop/native", "desktop/client", "desktop/media",
         "base_plugin", "desktop_utils", "file_utils")


def parameters(node):
    arguments = node.args
    names = [item.arg for item in arguments.posonlyargs + arguments.args + arguments.kwonlyargs]
    if arguments.vararg:
        names.append("*" + arguments.vararg.arg)
    if arguments.kwarg:
        names.append("**" + arguments.kwarg.arg)
    # Private parameters are internal to the SDK and stay out of the stubs.
    names = [name for name in names if not name.lstrip("*").startswith("_")]
    return names, isinstance(node, ast.AsyncFunctionDef)


def public_api(path):
    """{name: signature} of public functions and methods of public classes."""
    result = {}
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
            result[node.name] = parameters(node)
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            result[node.name] = "class"
            for item in node.body:
                if (isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                        and (not item.name.startswith("_") or item.name == "__init__")):
                    result[f"{node.name}.{item.name}"] = parameters(item)
    return result


class StubTests(unittest.TestCase):
    def test_stubs_match_modules(self):
        for name in STUBS:
            with self.subTest(module=name):
                source = public_api(SDK / f"{name}.py")
                stub = public_api(SDK / f"{name}.pyi")
                for key, signature in stub.items():
                    self.assertIn(key, source, f"{name}.pyi describes a missing {key}")
                    if signature != "class" and source[key] != "class":
                        self.assertEqual(signature, source[key], f"{name}: {key}")
                # Every public function of the module is described.
                missing = [key for key, value in source.items()
                           if "." not in key and key not in stub]
                self.assertEqual(missing, [], f"{name}.pyi misses")


if __name__ == "__main__":
    unittest.main()
