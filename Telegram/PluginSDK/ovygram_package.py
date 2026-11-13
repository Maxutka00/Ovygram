"""Static reading of .ovyplugin and .ovyzip packages: metadata, plugin ID
and version rules, ZIP safety. Nothing in a package is ever run.

Standard library only: the Ovygram client uses the same module, so both
sides read the same values from the same file (spec §5).
"""

import ast
import io
import json
import re
import stat
import zipfile
from dataclasses import dataclass
from pathlib import PurePosixPath

SDK_VERSION = 2
MAX_PACKAGE = 32 * 1024 * 1024
MAX_SOURCE = 1024 * 1024
MAX_ENTRIES = 512
MAX_RATIO = 100  # Uncompressed to compressed size of one ZIP entry.
MANIFEST = "plugin.json"
PACKAGE_TYPES = {".ovyplugin": "ovyplugin", ".ovyzip": "ovyzip"}

PLUGIN_ID = re.compile(r"[a-z0-9_]{1,25}\Z")
RESERVED_IDS = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)),
                *(f"lpt{i}" for i in range(1, 10))}
# The first part is a number; every part after a dot is a number with an
# optional Latin suffix (spec §6.1, §21 p. 1).
VERSION = re.compile(r"[0-9]+(\.[0-9]+[A-Za-z]*)*\Z")
VERSION_PART = re.compile(r"([0-9]+)([A-Za-z]*)\Z")

METADATA = {
    "__id__": "id", "__name__": "name", "__description__": "description",
    "__author__": "author", "__version__": "version", "__release__": "release",
    "__platform__": "platform", "__desktop_sdk__": "sdk",
    "__requirements__": "requirements",
}
REQUIRED = ("id", "name", "description", "author", "version", "release", "platform", "sdk")
TEXT_LIMITS = {"name": 128, "description": 2000, "author": 128}
WINDOWS_NAMES = {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$",
                 *(f"COM{i}" for i in "123456789¹²³"), *(f"LPT{i}" for i in "123456789¹²³")}


class InvalidPlugin(ValueError):
    """The message is shown to the author or the user."""


class IncompatiblePlugin(InvalidPlugin):
    """A valid SDK requirement that is newer than this application."""


# Plugin ID.

def normalize_id(value: object) -> str:
    if not isinstance(value, str):
        raise InvalidPlugin("ID плагина должен быть строкой.")
    plugin_id = value.lower()
    if not PLUGIN_ID.fullmatch(plugin_id):
        raise InvalidPlugin("ID плагина: латинские буквы, цифры и _, от 1 до 25 символов.")
    if plugin_id in RESERVED_IDS:
        raise InvalidPlugin(f"ID «{plugin_id}» — системное имя Windows.")
    return plugin_id


# Versions.

@dataclass(frozen=True)
class Version:
    text: str
    # Integer components without trailing zeros: 1.2 and 1.2.0 are (1, 2).
    numbers: tuple[int, ...]
    # Lowercase letter suffixes by component index, without empty ones:
    # 1.2b is ((1, "b"),). Two versions with equal numbers differ only here.
    suffix: tuple[tuple[int, str], ...]


def parse_version(value: object) -> Version:
    if not isinstance(value, str) or not value or len(value) > 15 or not VERSION.fullmatch(value):
        raise InvalidPlugin("Версия: до 15 символов, числа через точку, буквенный суффикс "
                            "только после точки (1, 1.2, 1.2b, 1.2.3inf).")
    numbers, suffix = [], []
    for index, part in enumerate(value.split(".")):
        number, letters = VERSION_PART.fullmatch(part).groups()
        numbers.append(int(number))
        if letters:
            suffix.append((index, letters.lower()))
    while len(numbers) > 1 and numbers[-1] == 0:
        numbers.pop()
    return Version(value, tuple(numbers), tuple(suffix))


def version_follows(new: Version, previous: Version) -> bool:
    """The new version may come after the previous approved one: higher
    numbers, or equal numbers with a different suffix (spec §6.1)."""
    if new.numbers != previous.numbers:
        return new.numbers > previous.numbers
    return new.suffix != previous.suffix


# Metadata.

def read_source(source: bytes, filename: str) -> dict:
    if len(source) > MAX_SOURCE:
        raise InvalidPlugin("Файл плагина больше 1 МиБ.")
    try:
        tree = ast.parse(source, filename=filename)
    except (SyntaxError, ValueError) as error:
        raise InvalidPlugin(f"Синтаксическая ошибка: {error}") from error
    values = {}
    simple = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            target = node.target
        else:
            continue
        if isinstance(target, ast.Name) and target.id in METADATA:
            if target.id in values:
                raise InvalidPlugin(f"Метатег {target.id} объявлен больше одного раза.")
            try:
                values[target.id] = ast.literal_eval(node.value)
            except ValueError as error:
                raise InvalidPlugin(f"{target.id} должен быть литералом.") from error
            simple.add(id(target))
    # Any other write to a metadata name makes the file ambiguous:
    # a, __id__ = ..., __id__ += ..., an assignment in a function or a loop.
    for node in ast.walk(tree):
        if (isinstance(node, ast.Name) and node.id in METADATA
                and isinstance(node.ctx, (ast.Store, ast.Del)) and id(node) not in simple):
            raise InvalidPlugin(f"Метатег {node.id} должен задаваться один раз простым присваиванием.")
    return check_metadata({METADATA[name]: value for name, value in values.items()})


def check_metadata(values: dict) -> dict:
    for key in REQUIRED:
        if key not in values:
            name = next(name for name, field in METADATA.items() if field == key)
            raise InvalidPlugin(f"Нет обязательного метатега {name}.")
    values["id"] = normalize_id(values["id"])
    for key, limit in TEXT_LIMITS.items():
        value = values[key]
        if not isinstance(value, str) or not value.strip() or len(value) > limit:
            raise InvalidPlugin(f"Поле {key}: непустая строка до {limit} символов.")
    values["version_info"] = parse_version(values["version"])
    if type(values["release"]) is not bool:
        raise InvalidPlugin("__release__ должен быть True или False.")
    if values["platform"] != "desktop":
        raise InvalidPlugin('Нужен __platform__ = "desktop".')
    if type(values["sdk"]) is not int or values["sdk"] < 1:
        raise InvalidPlugin(f"__desktop_sdk__: целое число от 1 до {SDK_VERSION}.")
    if values["sdk"] > SDK_VERSION:
        raise IncompatiblePlugin(f"Плагину требуется Desktop SDK {values['sdk']}, доступен {SDK_VERSION}.")
    requirements = values.get("requirements", [])
    if not isinstance(requirements, list) or len(requirements) > 32 \
            or not all(isinstance(item, str) and item.strip() for item in requirements):
        raise InvalidPlugin("__requirements__: список до 32 строк.")
    values["requirements"] = requirements
    return values


# Archives.

def archive_path(name: str) -> PurePosixPath:
    parts = name.split("/")
    if name.endswith("/"):
        parts.pop()
    if not parts or name.startswith("/") or any(
            not part or part in (".", "..") or part[-1] in " ."
            or re.search(r'[\\:<>"|?*\x00-\x1f]', part)
            or part.split(".")[0].rstrip(" ").upper() in WINDOWS_NAMES for part in parts):
        raise InvalidPlugin(f"Недопустимый путь внутри архива: {name!r}.")
    return PurePosixPath(*parts)


def read_member(archive: zipfile.ZipFile, entry: zipfile.ZipInfo, limit: int) -> bytes:
    # zipfile stops at the declared size and checks the CRC; one byte more
    # catches a member larger than the limit.
    with archive.open(entry) as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise InvalidPlugin(f"{entry.filename} больше допустимого размера.")
    return data


def read_zip(data: bytes) -> tuple[dict, list[str]]:
    """Metadata and the file list. Checks every entry (spec §13)."""
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as error:
        raise InvalidPlugin("Повреждённый архив.") from error
    with archive:
        entries = archive.infolist()
        if len(entries) > MAX_ENTRIES:
            raise InvalidPlugin(f"В архиве больше {MAX_ENTRIES} записей.")
        if sum(entry.file_size for entry in entries) > MAX_PACKAGE:
            raise InvalidPlugin("Распакованный архив больше 32 МиБ.")
        files: dict[str, zipfile.ZipInfo] = {}
        folded = set()
        for entry in entries:
            path = archive_path(entry.orig_filename)
            key = path.as_posix().casefold()
            if key in folded:
                raise InvalidPlugin(f"Повторный путь в архиве: {entry.orig_filename!r}.")
            folded.add(key)
            # Only the file type bits: many tools store bare permissions.
            kind = stat.S_IFMT(entry.external_attr >> 16)
            if kind not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise InvalidPlugin(f"Ссылка или специальный файл в архиве: {entry.orig_filename!r}.")
            if entry.flag_bits & 0x1:
                raise InvalidPlugin("Зашифрованные записи не поддерживаются.")
            if entry.file_size > 1024 * 1024 and entry.file_size > MAX_RATIO * max(entry.compress_size, 1):
                raise InvalidPlugin(f"Слишком сильное сжатие: {entry.orig_filename!r}.")
            if not entry.is_dir():
                files[path.as_posix()] = entry
        if MANIFEST not in files:
            raise InvalidPlugin(f"В корне архива нужен {MANIFEST}.")
        try:
            manifest = json.loads(read_member(archive, files[MANIFEST], 4096))
        except ValueError as error:
            raise InvalidPlugin(f"{MANIFEST} — некорректный JSON.") from error
        if not isinstance(manifest, dict) or set(manifest) != {"id", "entry"}:
            raise InvalidPlugin(f"{MANIFEST} должен содержать ровно поля id и entry.")
        entry = manifest["entry"]
        if not isinstance(entry, str) or "/" in entry or entry not in files \
                or not entry.endswith((".py", ".ovyplugin")):
            raise InvalidPlugin("Точка входа — файл .py или .ovyplugin в корне архива.")
        metadata = read_source(read_member(archive, files[entry], MAX_SOURCE), entry)
        if normalize_id(manifest["id"]) != metadata["id"]:
            raise InvalidPlugin(f"ID в {MANIFEST} не совпадает с __id__ точки входа.")
        metadata["entry"] = entry
        return metadata, sorted(files)


def package_type(filename: str) -> str:
    for suffix, kind in PACKAGE_TYPES.items():
        if filename.endswith(suffix):
            return kind
    raise InvalidPlugin("Ожидается файл .ovyplugin или .ovyzip.")


def read_package(data: bytes, filename: str, strict_name: bool = True) -> dict:
    """Metadata of a package with "package_type". strict_name requires the
    file to be named <plugin_id>.ovyplugin or <plugin_id>.ovyzip, as for
    submissions (spec §4)."""
    kind = package_type(filename)
    if len(data) > MAX_PACKAGE:
        raise InvalidPlugin("Файл больше 32 МиБ.")
    if kind == "ovyzip":
        metadata, _ = read_zip(data)
    else:
        metadata = read_source(data, filename)
    expected = f"{metadata['id']}.{kind}"
    if strict_name and filename != expected:
        raise InvalidPlugin(f"Файл должен называться {expected}.")
    metadata["package_type"] = kind
    return metadata
