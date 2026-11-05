"""Generate the desktop TL catalogue and editor types from the pinned schema."""

import argparse
import hashlib
import json
import keyword
from pathlib import Path
import re


DECLARATION = re.compile(r"^([\w.]+)#([0-9a-f]+)\s*(.*?)\s*=\s*([^;]+);$")


def python_name(name):
    return name + "_" if keyword.iskeyword(name) or name == "self" else name


def parse_schema(text):
    declarations = []
    functions = False
    for raw in text.splitlines():
        line = raw.split("//", 1)[0].strip()
        if not line:
            continue
        if line == "---functions---":
            functions = True
            continue
        if line == "---types---":
            functions = False
            continue
        if line.startswith("vector#"):
            continue
        match = DECLARATION.fullmatch(line)
        if match is None:
            raise ValueError(f"Unsupported TL declaration: {line}")
        name, constructor, fields, result = match.groups()
        fields = re.sub(r"\{[^}]*\}", "", fields)
        parameters = []
        for field in fields.split():
            key, value = field.split(":", 1)
            parameters.append([key, value])
        declarations.append({
            "name": name, "id": int(constructor, 16), "fields": parameters,
            "result": result.strip(), "function": functions,
        })
    ids = [item["id"] for item in declarations]
    names = [item["name"] for item in declarations]
    if len(ids) != len(set(ids)) or len(names) != len(set(names)):
        raise ValueError("Duplicate TL declaration.")
    return declarations


def annotation(value):
    optional = "?" in value
    value = value.split("?", 1)[-1]
    vector = re.fullmatch(r"[Vv]ector<(.+)>", value)
    if vector:
        result = f"list[{annotation(vector[1])}]"
    else:
        result = {
            "int": "int", "long": "int", "#": "int", "double": "float",
            "string": "str", "bytes": "bytes", "int128": "int | bytes",
            "int256": "int | bytes", "Bool": "bool", "true": "bool",
        }.get(value, "TLObject")
    return result + " | None" if optional and result != "bool" else result


def stubs(declarations):
    lines = ["from .codec import (TLObject as TLObject, constructor as constructor,",
             "                    decode as decode, encode as encode, response_type as response_type)", ""]
    tree = {}
    for declaration in declarations:
        children = tree
        for part in declaration["name"].split("."):
            node = children.setdefault(part, {"children": {}})
            children = node["children"]
        node["declaration"] = declaration

    def emit(nodes, indent=""):
        for name, node in sorted(nodes.items()):
            declaration = node.get("declaration")
            parent = "(TLObject)" if declaration else ""
            lines.append(f"{indent}class {python_name(name)}{parent}:")
            if not declaration:
                emit(node["children"], indent + "    ")
                continue
            fields = [(python_name(key), value) for key, value in declaration["fields"]
                      if value != "#"]
            for key, value in fields:
                lines.append(f"{indent}    {key}: {annotation(value)}")
            arguments = []
            for key, value in fields:
                default = " = ..." if "?" in value else ""
                arguments.append(f"{key}: {annotation(value)}{default}")
            parameters = ", *, " + ", ".join(arguments) if arguments else ""
            lines.append(f"{indent}    def __init__(self{parameters}) -> None: ...")
            emit(node["children"], indent + "    ")
            lines.append("")
    emit(tree)
    return "\n".join(lines)


def generate(schema, output):
    data = schema.read_text(encoding="utf-8").encode("utf-8")
    declarations = parse_schema(data.decode("utf-8"))
    output.mkdir(parents=True, exist_ok=True)
    catalogue = {"schema_sha256": hashlib.sha256(data).hexdigest(),
                 "declarations": declarations}
    (output / "schema.json").write_text(
        json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "__init__.pyi").write_text(stubs(declarations), encoding="utf-8")
    return len(declarations)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    print(f"Generated {generate(arguments.schema, arguments.output)} TL declarations.")
