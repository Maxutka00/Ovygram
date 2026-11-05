"""Strict TL encoding shared by requests, events and transactional hooks."""

import copy
import keyword
from pathlib import Path
import json
import re
import struct
from types import SimpleNamespace


VECTOR = 0x1CB5C415
BOOL_TRUE = 0x997275B5
BOOL_FALSE = 0xBC799737
MAX_BYTES = 64 * 1024 * 1024
MAX_ITEMS = 1_000_000
MAX_DEPTH = 128
_by_id = {}
_by_name = {}


def python_name(name):
    return name + "_" if keyword.iskeyword(name) or name == "self" else name


class TLObject:
    _tl = None

    def __init__(self, **values):
        expected = {python_name(name) for name, _ in self._tl["fields"]}
        unknown = values.keys() - expected
        if unknown:
            raise TypeError(f"Unknown {self._tl['name']} fields: {sorted(unknown)}")
        for name, kind in self._tl["fields"]:
            key = python_name(name)
            if key not in values and kind != "#" and "?" not in kind:
                raise TypeError(f"Required field {self._tl['name']}.{key}")
            default = 0 if kind == "#" else False if kind.endswith("?true") else None
            setattr(self, key, values.get(key, default))

    def __repr__(self):
        values = ", ".join(f"{python_name(name)}={getattr(self, python_name(name))!r}"
                           for name, kind in self._tl["fields"] if kind != "#")
        return f"{self._tl['name']}({values})"

    def __eq__(self, other):
        return type(self) is type(other) and encode(self) == encode(other)

    def clone(self, **changes):
        result = copy.deepcopy(self)
        for key, value in changes.items():
            if key not in result.__dict__:
                raise TypeError(f"Unknown field {key}")
            setattr(result, key, value)
        return result

    @property
    def constructor_name(self):
        return self._tl["name"]


def load_catalogue(namespace):
    catalogue = json.loads(Path(__file__).with_name("schema.json").read_text(encoding="utf-8"))
    for declaration in catalogue["declarations"]:
        name = declaration["name"]
        generated = type(python_name(name.rsplit(".", 1)[-1]), (TLObject,),
                         {"_tl": declaration, "__module__": "desktop.tl"})
        _by_id[declaration["id"]] = generated
        _by_name[name] = generated
        container = namespace
        parts = name.split(".")
        for part in parts[:-1]:
            part = python_name(part)
            current = container.get(part) if isinstance(container, dict) else getattr(container, part, None)
            if current is None:
                current = SimpleNamespace()
                if isinstance(container, dict):
                    container[part] = current
                else:
                    setattr(container, part, current)
            container = current
        if isinstance(container, dict):
            key = python_name(parts[-1])
            previous = container.get(key)
            if isinstance(previous, SimpleNamespace):
                for member, value in vars(previous).items():
                    setattr(generated, member, value)
            container[key] = generated
        else:
            setattr(container, python_name(parts[-1]), generated)
    return catalogue["schema_sha256"]


def constructor(name):
    return _by_name[name]


def response_type(request):
    result = request._tl["result"]
    if result in ("X", "!X"):
        query = next((getattr(request, python_name(name))
                      for name, kind in request._tl["fields"] if kind == "!X"), None)
        if not isinstance(query, TLObject):
            raise TypeError("Generic RPC requires a typed query.")
        return response_type(query)
    return result


def _bytes(value):
    size = len(value)
    if size >= 2 ** 24:
        raise ValueError("TL bytes exceeds 24-bit length.")
    header = bytes([size]) if size < 254 else b"\xfe" + size.to_bytes(3, "little")
    return header + value + b"\x00" * (-(len(header) + size) % 4)


def _encode(value, kind, depth):
    if depth > MAX_DEPTH:
        raise ValueError("TL nesting limit exceeded.")
    vector = re.fullmatch(r"[Vv]ector<(.+)>", kind)
    if vector:
        if not isinstance(value, (list, tuple)) or len(value) > MAX_ITEMS:
            raise ValueError("Invalid TL vector.")
        prefix = struct.pack("<I", VECTOR) if kind.startswith("Vector") else b""
        return prefix + struct.pack("<i", len(value)) + b"".join(
            _encode(item, vector[1], depth + 1) for item in value)
    if kind in ("int", "long", "#"):
        if type(value) is not int:
            raise TypeError(f"{kind} requires int.")
        bits = 64 if kind == "long" else 32
        if not -(2 ** (bits - 1)) <= value < 2 ** bits:
            raise ValueError(f"{kind} overflow.")
        return (value % 2 ** bits).to_bytes(bits // 8, "little")
    if kind in ("int128", "int256"):
        size = int(kind[3:]) // 8
        result = value.to_bytes(size, "little") if isinstance(value, int) else bytes(value)
        if len(result) != size:
            raise ValueError(f"Invalid {kind} length.")
        return result
    if kind == "double":
        return struct.pack("<d", value)
    if kind in ("string", "bytes"):
        if (kind == "string" and not isinstance(value, str)
                or kind == "bytes" and not isinstance(value, (bytes, bytearray, memoryview))):
            raise TypeError(f"{kind} requires {'str' if kind == 'string' else 'bytes'}.")
        result = value.encode("utf-8") if kind == "string" else bytes(value)
        return _bytes(result)
    if kind == "Bool":
        if type(value) is not bool:
            raise TypeError("Bool requires bool.")
        return struct.pack("<I", BOOL_TRUE if value else BOOL_FALSE)
    if kind == "true":
        return b""
    if not isinstance(value, TLObject):
        raise TypeError(f"{kind} requires a TL object.")
    if (kind not in ("Object", "X", "!X") and not kind.startswith("!")
            and value._tl["result"] != kind):
        raise TypeError(f"Expected {kind}, got {value._tl['result']}.")
    return _encode_object(value, depth + 1)


def _encode_object(value, depth):
    fields = value._tl["fields"]
    flags = {name: getattr(value, python_name(name)) for name, kind in fields if kind == "#"}
    groups = {}
    for name, kind in fields:
        if "?" not in kind:
            continue
        flag, _ = kind.split("?", 1)
        variable, bit = flag.split(".")
        present = getattr(value, python_name(name))
        present = bool(present) if kind.endswith("?true") else present is not None
        groups.setdefault((variable, int(bit)), []).append(present)
    for (variable, bit), values in groups.items():
        if any(values) != all(values):
            raise ValueError(f"Fields sharing {variable}.{bit} must be set together.")
        flags[variable] = (flags[variable] & ~(1 << bit)) | (int(all(values)) << bit)
    result = [struct.pack("<I", value._tl["id"])]
    for name, kind in fields:
        item = flags[name] if kind == "#" else getattr(value, python_name(name))
        if "?" in kind:
            flag, kind = kind.split("?", 1)
            variable, bit = flag.split(".")
            if not flags[variable] & (1 << int(bit)):
                continue
        result.append(_encode(item, kind, depth))
    return b"".join(result)


def encode(value):
    result = _encode(value, "Object", 0)
    if len(result) > MAX_BYTES:
        raise ValueError("TL payload limit exceeded.")
    return result


class Reader:
    def __init__(self, data):
        if len(data) > MAX_BYTES:
            raise ValueError("TL payload limit exceeded.")
        self.data = memoryview(data)
        self.position = 0

    def take(self, size):
        if size < 0 or size > len(self.data) - self.position:
            raise ValueError("Truncated TL payload.")
        result = self.data[self.position:self.position + size].tobytes()
        self.position += size
        return result

    def read(self, kind="Object", depth=0):
        if depth > MAX_DEPTH:
            raise ValueError("TL nesting limit exceeded.")
        vector = re.fullmatch(r"[Vv]ector<(.+)>", kind)
        if vector:
            if kind.startswith("Vector") and int.from_bytes(self.take(4), "little") != VECTOR:
                raise ValueError("Invalid TL vector constructor.")
            count = int.from_bytes(self.take(4), "little", signed=True)
            if not 0 <= count <= MAX_ITEMS:
                raise ValueError("Invalid TL vector count.")
            return [self.read(vector[1], depth + 1) for _ in range(count)]
        if kind in ("int", "long", "#", "double", "int128", "int256"):
            size = {"int": 4, "long": 8, "#": 4, "double": 8, "int128": 16, "int256": 32}[kind]
            data = self.take(size)
            if kind == "double":
                return struct.unpack("<d", data)[0]
            if kind in ("int128", "int256"):
                return data
            return int.from_bytes(data, "little", signed=kind != "#")
        if kind in ("string", "bytes"):
            first = self.take(1)[0]
            if first == 255:
                raise ValueError("Invalid TL bytes prefix.")
            size = int.from_bytes(self.take(3), "little") if first == 254 else first
            value = self.take(size)
            padding = (-(size + (4 if first == 254 else 1))) % 4
            self.take(padding)
            return value.decode("utf-8") if kind == "string" else value
        if kind == "true":
            return True
        identity = int.from_bytes(self.take(4), "little")
        if kind == "Bool":
            if identity not in (BOOL_TRUE, BOOL_FALSE):
                raise ValueError("Invalid TL Bool.")
            return identity == BOOL_TRUE
        generated = _by_id.get(identity)
        if generated is None:
            raise ValueError(f"Unknown TL constructor {identity:#x}.")
        if (kind not in ("Object", "X", "!X") and not kind.startswith("!")
                and generated._tl["result"] != kind):
            raise TypeError(f"Expected {kind}, got {generated._tl['result']}.")
        fields = {}
        for name, field_kind in generated._tl["fields"]:
            if "?" in field_kind:
                flag, field_kind = field_kind.split("?", 1)
                variable, bit = flag.split(".")
                if not fields[python_name(variable)] & (1 << int(bit)):
                    fields[python_name(name)] = False if field_kind == "true" else None
                    continue
            fields[python_name(name)] = self.read(field_kind, depth + 1)
        return generated(**fields)


def decode(data, result="Object"):
    reader = Reader(data)
    value = reader.read(result)
    if reader.position != len(reader.data):
        raise ValueError("Trailing TL payload data.")
    return value
