"""The process-wide Python side of the desktop plugin host.

Installed plugins are installations: each has a random installation_id that
keys its state, settings, data, handlers and errors. Several installations
may share one plugin_id (spec §3.2); an update keeps the installation_id.
"""

import ast
import copy
import hashlib
import importlib.util
import inspect
import io
import json
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import threading
import uuid
import zipfile

from base_plugin import BasePlugin
from desktop._runtime import Runtime
from hook_utils import HookCancelled
from ovygram_deps import Dependencies, normalize_all
from ovygram_distribution import Distribution
from ovygram_registry import TRUSTED, protected_author
from ovygram_package import (MAX_PACKAGE, MAX_SOURCE, SDK_VERSION, archive_path, read_source,
                             read_zip)
from ui.settings import Button, Header, Input, Selector, Switch


STATE_VERSION = 2
INSTALLATION_ID = re.compile(r"[0-9a-f]{32}\Z")
VERSION_DIR = re.compile(r"[0-9a-f]{32}\Z")
# The package formats of the ecosystem and the local-only extra ones; every
# one is read with the same metadata rules.
SINGLE = (".ovyplugin", ".py", ".plugin")
ARCHIVE = (".ovyzip", ".zip")
STORED_FIELDS = ("id", "name", "description", "author", "version", "release", "platform", "sdk",
                 "requirements")


def plugin_metadata(source, filename):
    """Metadata of a single plugin file as stored in its installation."""
    return stored(read_source(source, filename))


def stored(values):
    metadata = {key: values[key] for key in STORED_FIELDS}
    metadata["requirements"] = normalize_all(metadata["requirements"])
    return metadata


# Plugins installed before installations existed keep their old metadata
# rules until they are updated from a file.
LEGACY_ID = re.compile(r"[a-z][a-z0-9_.-]{0,63}\Z")
LEGACY_METADATA = {
    "__id__": "id", "__name__": "name", "__version__": "version",
    "__author__": "author", "__description__": "description",
    "__platform__": "platform", "__desktop_sdk__": "sdk",
    "__requirements__": "requirements",
}


def legacy_metadata(source, filename):
    if len(source) > MAX_SOURCE:
        raise ValueError("Файл плагина больше 1 МиБ.")
    values = {}
    for node in ast.parse(source, filename=filename).body:
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets = [node.target]
        else:
            continue
        for target in targets:
            if isinstance(target, ast.Name) and target.id in LEGACY_METADATA:
                key = LEGACY_METADATA[target.id]
                if key in values:
                    raise ValueError(f"Метаданные {target.id} указаны дважды.")
                values[key] = ast.literal_eval(node.value)
    for key in ("id", "name", "version", "author", "description"):
        if not isinstance(values.get(key), str) or not values[key].strip():
            raise ValueError(f"Укажите строковое поле {key} в метаданных.")
    if not LEGACY_ID.fullmatch(values["id"]):
        raise ValueError("Недопустимый ID плагина.")
    if values.get("platform") != "desktop":
        raise ValueError('Укажите __platform__ = "desktop". Android-плагины требуют переноса.')
    if type(values.get("sdk")) is not int or not 1 <= values["sdk"] <= SDK_VERSION:
        raise ValueError(f"Поддерживаются версии Desktop SDK от 1 до {SDK_VERSION}.")
    if "requirements" in values:
        values["requirements"] = normalize_all(values["requirements"])
    return values


def read_package(payload, filename):
    """(metadata, package type) of a package without running it."""
    suffix = PurePosixPath(filename).suffix.lower()
    if suffix in SINGLE:
        return plugin_metadata(payload, filename), "ovyplugin"
    if suffix in ARCHIVE:
        values, _ = read_zip(payload)
        return stored(values), "ovyzip"
    raise ValueError("Выберите файл .ovyplugin или .ovyzip.")


def unpack_package(payload, kind, target):
    """Writes a checked package into its version directory; returns the
    entry point."""
    if kind == "ovyplugin":
        (target / "plugin.py").write_bytes(payload)
        return "plugin.py"
    _, names = read_zip(payload)
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        entry = json.loads(archive.read("plugin.json"))["entry"]
        for name in names:
            destination = target.joinpath(*archive_path(name).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(name) as reader, destination.open("xb") as writer:
                shutil.copyfileobj(reader, writer)
    return entry


class PluginContext:
    def __init__(self, manager, installation_id, plugin_id):
        self.manager = manager
        self.installation_id = installation_id
        self.plugin_id = plugin_id
        self.active = True

    def get(self, key, default, account_id=None):
        self.check_active()
        record = self.manager.records[self.installation_id]
        settings = record["settings"] if account_id is None else record.get(
            "account_settings", {}).get(self.manager.account_key(account_id), {})
        return copy.deepcopy(settings.get(key, default))

    def set(self, key, value, account_id=None):
        self.check_active()
        self.manager.check_thread()
        self.manager.set_setting(self.installation_id, key, value, account_id)

    def log(self, message):
        self.check_active()
        self.manager.logger.info("%s: %s", self.manager.label(self.installation_id), message)

    def check_active(self):
        if not self.active:
            raise RuntimeError("Плагин уже выгружен.")


class Manager:
    def __init__(self, root, disabled=False, registry=None):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.packages = self.root / "packages"
        self.packages.mkdir(exist_ok=True)
        self.state = self.root / "state.json"
        self.marker = self.root / "running"
        self.disabled = disabled
        self.recovery = self.marker.exists()
        self.restart_required = False
        self.owner = threading.get_ident()
        self.loaded = {}
        self.errors = {}
        self.setting_actions = {}
        self.distribution_state = {}
        self.pending_updates = {}
        self.logger = logging.Logger("ovygram")
        self.log_handler = RotatingFileHandler(
            self.root / "plugins.log", maxBytes=1024 * 1024, backupCount=2,
            encoding="utf-8",
        )
        self.log_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        self.logger.addHandler(self.log_handler)
        self.runtime = Runtime(self)
        # The SDK lies in python/sdk, next to the bundled interpreter and pip.
        self.dependencies = Dependencies(self.root, Path(__file__).resolve().parent.parent)
        self.records = self.read_state()
        self.distribution = Distribution(self, registry)
        self.recover_updates()
        if not (self.disabled or self.recovery):
            for installation_id, record in self.records.items():
                if record["enabled"]:
                    self.load(installation_id)

    def read_state(self):
        state = json.loads(self.state.read_text(encoding="utf-8")) if self.state.exists() else {
            "version": STATE_VERSION, "installations": {}}
        if isinstance(state, dict) and "version" not in state:
            state = self.migrate(state)
        records = state.get("installations") if isinstance(state, dict) else None
        if state.get("version") != STATE_VERSION or not isinstance(records, dict) or any(
            not INSTALLATION_ID.fullmatch(installation_id) or not isinstance(record, dict)
            or not {"plugin_id", "current", "previous", "enabled", "settings"} <= record.keys()
            for installation_id, record in records.items()
        ):
            raise ValueError("Повреждён файл состояния плагинов.")
        self.distribution_state = state.get("distribution", {})
        self.pending_updates = state.get("pending_updates", {})
        if not isinstance(self.pending_updates, dict) or any(
                identity not in records or not isinstance(previous, dict)
                or not {"plugin_id", "current", "previous", "enabled", "settings"} <= previous.keys()
                or previous["plugin_id"] != records[identity]["plugin_id"]
                for identity, previous in self.pending_updates.items()):
            raise ValueError("Повреждён журнал обновлений плагинов.")
        return records

    def recover_updates(self):
        """Before any plugin executes, restore operations lacking a commit.

        The old code/settings snapshot is durable before code is replaced.
        The existing crash marker still requires the normal recovery consent.
        """
        for identity, previous in tuple(self.pending_updates.items()):
            interrupted = self.records[identity]
            self.change_record(identity, copy.deepcopy(previous))
            self.finish_update(identity)
            keep = {version["directory"] for version in (previous["current"], previous["previous"]) if version}
            for version in (interrupted["current"], interrupted["previous"]):
                if version and version["directory"] not in keep:
                    try:
                        self.discard(version)
                    except OSError as error:
                        self.logger.warning("Не удалось удалить прерванное обновление: %s", error)
            self.logger.warning("Восстановлена предыдущая версия после прерванного обновления: %s", identity)

    def finish_update(self, identity):
        previous = self.pending_updates.pop(identity)
        try:
            self.save()
        except BaseException:
            self.pending_updates[identity] = previous
            raise

    def migrate(self, records):
        """State of the first format, keyed by plugin_id: every plugin
        becomes an installation, its data directory moves along."""
        if any(not isinstance(record, dict) or not LEGACY_ID.fullmatch(plugin_id)
               for plugin_id, record in records.items()):
            raise ValueError("Повреждён файл состояния плагинов.")
        installations = {}
        for plugin_id, record in records.items():
            installation_id = uuid.uuid4().hex
            for key in ("current", "previous"):
                if record.get(key):
                    record[key]["format"] = "legacy"
            installations[installation_id] = {**record, "plugin_id": plugin_id}
            data = self.root / "data" / plugin_id
            if data.is_dir():
                data.rename(self.root / "data" / installation_id)
        state = {"version": STATE_VERSION, "installations": installations}
        self.records = installations
        self.save()
        return state

    def label(self, installation_id):
        record = self.records.get(installation_id)
        return f"{record['plugin_id']}[{installation_id[:8]}]" if record else installation_id

    def check_thread(self):
        if threading.get_ident() != self.owner:
            raise RuntimeError("Настройки плагина доступны только в главном потоке.")

    def save(self):
        text = json.dumps({"version": STATE_VERSION, "installations": self.records,
                           "distribution": self.distribution_state, "pending_updates": self.pending_updates},
                          ensure_ascii=False, allow_nan=False, indent=2)
        temporary = self.state.with_suffix(".tmp")
        with temporary.open("w", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(self.state)

    def directory(self, version):
        token = version["directory"]
        if not VERSION_DIR.fullmatch(token):
            raise ValueError("Недопустимый каталог версии плагина.")
        path = self.packages / token
        if path.resolve() != self.root / "packages" / token:
            raise ValueError("Каталог версии выходит за пределы профиля плагинов.")
        return path

    def discard(self, version):
        if version:
            path = self.directory(version)
            if path.exists():
                shutil.rmtree(path)
            share = self.share_directory(version)
            if share.exists():
                shutil.rmtree(share)

    def share_directory(self, version):
        token = self.directory(version).name
        path = self.root / "share" / token
        if path.resolve() != path:
            raise ValueError("Каталог отправки выходит за пределы профиля плагинов.")
        return path

    def original(self, version):
        """The installed package file exactly as it was imported."""
        name = version.get("share_file")
        record_id = version.get("metadata", {}).get("id", "")
        allowed = {f"{record_id}.{version.get('package_type')}",
                   *(f"plugin-{record_id}{suffix}" for suffix in (".py", ".plugin", ".zip"))}
        if name is None or name not in allowed:
            raise ValueError("Недопустимое имя файла плагина.")
        target = self.share_directory(version) / name
        if target.resolve() != target or not target.is_file():
            raise ValueError("Исходный пакет плагина отсутствует. Обнови плагин из файла.")
        return target

    def share_file(self, installation_id):
        version = self.records[installation_id]["current"]
        if version.get("share_file") is None:
            share = self.share_directory(version)
            package = self.directory(version)
            plugin_id = self.records[installation_id]["plugin_id"]
            if version["entry"] != "plugin.py" or (package / "plugin.json").exists():
                raise ValueError("Обнови ZIP-плагин из исходного архива, чтобы отправить его.")
            source = package / "plugin.py"
            if source.resolve() != source or source.stat().st_size > MAX_SOURCE:
                raise ValueError("Недопустимый файл плагина.")
            share.mkdir(parents=True, exist_ok=True)
            target = share / f"plugin-{plugin_id}.plugin"
            if target.resolve() != target:
                raise ValueError("Недопустимый путь отправки плагина.")
            shutil.copyfile(source, target)
            return str(target)
        return str(self.original(version))

    def check_integrity(self, version):
        """The installed files are still the package that was checked: a
        local replacement must not keep its trust status (spec §3.3)."""
        if "sha256" not in version:
            return  # Installed before hashes were kept.
        payload = self.original(version).read_bytes()
        if hashlib.sha256(payload).hexdigest() != version["sha256"]:
            raise ValueError("Файл плагина изменён после установки. Установите его заново.")
        directory = self.directory(version)
        if version["package_type"] == "ovyplugin":
            expected = {"plugin.py": payload}
        else:
            with zipfile.ZipFile(io.BytesIO(payload)) as archive:
                expected = {name: archive.read(name) for name in read_zip(payload)[1]}
        for name, data in expected.items():
            path = directory.joinpath(*PurePosixPath(name).parts)
            if path.resolve() != path or not path.is_file() or path.read_bytes() != data:
                raise ValueError(f"Файл {name} плагина изменён после установки. Установите его заново.")
        for path in directory.rglob("*"):
            if path.is_symlink() or (path.is_file() and path.relative_to(directory).as_posix() not in expected
                                    and path.suffix.lower() in (".py", ".pyc", ".pyo", ".so", ".dll", ".pyd", ".ovyplugin")):
                raise ValueError("В каталоге плагина появился посторонний исполняемый файл.")
        return expected.get(version["entry"])

    def report_error(self, installation_id, message):
        self.errors[installation_id] = message
        self.logger.exception("%s: %s", self.label(installation_id), message)

    def call(self, installation_id, method, *args):
        return self.runtime.call(self.runtime.contexts[installation_id], method, *args)

    def load(self, installation_id):
        record = self.records[installation_id]
        version = record["current"]
        namespace = "_ovygram_" + version["directory"]
        context = PluginContext(self, installation_id, record["plugin_id"])
        self.runtime.contexts[installation_id] = context
        self.marker.write_text(installation_id, encoding="utf-8")
        try:
            if version.get("blocked") or self.distribution.registry.cached(version)["status"] == "blocked":
                raise ValueError("Опасный плагин / вирус: запуск запрещён.")
            requirements = version["metadata"].get("requirements", [])
            if not self.dependencies.satisfied(requirements):
                if self.dependencies.waiting_for_restart(requirements):
                    raise RuntimeError("Зависимости установлены. Перезапустите клиент.")
                raise RuntimeError("Зависимости не установлены. Выключите и снова включите плагин.")
            checked_source = self.check_integrity(version)
            directory = self.directory(version)
            entry = version["entry"]
            if len(archive_path(entry).parts) != 1:
                raise ValueError("Недопустимая точка входа.")
            path = directory / entry
            if path.resolve().parent != directory:
                raise ValueError("Точка входа выходит за пределы каталога плагина.")
            spec = importlib.util.spec_from_loader(namespace, loader=None, is_package=True)
            module = importlib.util.module_from_spec(spec)
            module.__file__ = str(path)
            module.__path__ = [str(directory)]
            sys.modules[namespace] = module
            if checked_source is None:
                with path.open("rb") as stream:
                    source = stream.read(MAX_SOURCE + 1)
            else:
                source = checked_source
            reader = legacy_metadata if version.get("format") == "legacy" else plugin_metadata
            if reader(source, str(path)) != version["metadata"]:
                raise ValueError("Метаданные изменились. Импортируйте новую версию из файла.")
            exec(compile(source, str(path), "exec"), module.__dict__)
            classes = {
                value for value in module.__dict__.values()
                if isinstance(value, type) and value is not BasePlugin
                and issubclass(value, BasePlugin)
                and value.__module__ in (namespace, version["metadata"]["name"])
            }
            if len(classes) != 1:
                raise ValueError("В точке входа должен быть один класс BasePlugin.")
            instance = classes.pop()()
            instance._desktop_context = context
            self.call(installation_id, instance.on_plugin_load)
            self.loaded[installation_id] = (instance, context, namespace)
            self.errors.pop(installation_id, None)
            return True
        except BaseException as error:
            context.active = False
            self.runtime.remove(installation_id)
            self.clear_modules(namespace)
            message = str(error) or type(error).__name__
            if isinstance(error, ModuleNotFoundError) and (error.name or "").split(".")[0] in {
                "android", "java", "jnius", "chaquopy", "org",
            }:
                message = "Этот импорт относится к Android. Адаптируйте плагин для Desktop SDK."
            self.report_error(installation_id, message)
            return False

    @staticmethod
    def clear_modules(namespace):
        for name in tuple(sys.modules):
            if name == namespace or name.startswith(namespace + "."):
                sys.modules.pop(name, None)

    def unload(self, installation_id):
        if installation_id not in self.loaded:
            return
        instance, context, namespace = self.loaded.pop(installation_id)
        try:
            self.call(installation_id, instance.on_plugin_unload)
        except BaseException as error:
            self.restart_required = True
            self.report_error(installation_id, str(error) or type(error).__name__)
            raise RuntimeError("Выгрузка завершилась ошибкой. Перезапустите клиент.") from error
        finally:
            self.setting_actions = {key: value for key, value in self.setting_actions.items()
                                    if key[0] != installation_id}
            context.active = False
            self.runtime.remove(installation_id)
            self.clear_modules(namespace)

    def change_record(self, installation_id, record):
        previous = self.records.get(installation_id)
        if record is None:
            del self.records[installation_id]
        else:
            self.records[installation_id] = record
        try:
            self.save()
        except BaseException:
            if previous is None:
                self.records.pop(installation_id, None)
            else:
                self.records[installation_id] = previous
            raise

    @staticmethod
    def read_file(path):
        source = Path(path)
        suffix = source.suffix.lower()
        if suffix not in SINGLE + ARCHIVE:
            raise ValueError("Выберите файл .ovyplugin или .ovyzip.")
        limit = MAX_PACKAGE if suffix in ARCHIVE else MAX_SOURCE
        with source.open("rb") as stream:
            payload = stream.read(limit + 1)
        if len(payload) > limit:
            raise ValueError("Файл плагина превышает допустимый размер.")
        return payload

    def installations_of(self, plugin_id):
        return [installation_id for installation_id, record in self.records.items()
                if record["plugin_id"] == plugin_id]

    def inspect(self, path):
        """What the install dialog shows about a file, without running it:
        metadata, the exact hash and the installations with the same ID."""
        payload = self.read_file(path)
        metadata, kind = read_package(payload, Path(path).name)
        return {
            "metadata": metadata, "package_type": kind,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "installations": [self.describe(installation_id)
                              for installation_id in self.installations_of(metadata["id"])],
        }

    def install(self, path, installation_id="", separate=False):
        """Installs a file as a new installation, or updates installation_id
        keeping its ID, settings and data. A plugin_id that is already
        installed needs either installation_id or separate=True."""
        payload = self.read_file(path)
        metadata, kind = read_package(payload, Path(path).name)
        return self.install_bytes(payload, metadata, kind, installation_id, separate)

    def install_bytes(self, payload, metadata, kind, installation_id="", separate=False,
                      trust=None, allow_loss=False):
        # Callers supply already parsed bytes, never a path fetched a second time.
        registry = self.distribution.registry
        trust = trust or {"status": "verification_unavailable"}
        if trust["status"] == "blocked":
            raise ValueError("Опасный плагин / вирус: установка запрещена.")
        plugin_id = metadata["id"]
        existing = self.installations_of(plugin_id)
        if trust["status"] in TRUSTED and any(
                identity != installation_id and registry.cached(self.records[identity]["current"])["status"]
                in TRUSTED for identity in existing):
            raise ValueError("Два проверенных экземпляра с одинаковым ID запрещены. Обновите существующий.")
        previous = self.records.get(installation_id) if installation_id else None
        if previous and previous["current"].get("trust", {}).get("status") in TRUSTED \
                and trust["status"] not in TRUSTED and not allow_loss:
            raise ValueError("Требуется отдельное подтверждение потери проверки.")
        token = uuid.uuid4().hex
        version = {"directory": token}
        directory = self.directory(version)
        directory.mkdir()
        try:
            if installation_id:
                previous = self.records.get(installation_id)
                if previous is None:
                    raise ValueError("Установленный экземпляр не найден.")
                if previous["plugin_id"] != plugin_id:
                    raise ValueError("ID обновления отличается от ID установленного плагина.")
            elif self.installations_of(plugin_id) and not separate:
                raise ValueError("Плагин с таким ID уже установлен: обновите его или установите отдельно.")
            else:
                previous = None
                installation_id = uuid.uuid4().hex
            share = self.share_directory(version)
            share.mkdir(parents=True)
            name = f"{plugin_id}.{kind}"
            (share / name).write_bytes(payload)
            entry = unpack_package(payload, kind, directory)
            version.update(metadata=metadata, entry=entry, share_file=name, package_type=kind,
                           sha256=hashlib.sha256(payload).hexdigest(), trust=trust,
                           blocked=False)
            if previous:
                self.unload(installation_id)
                previous = self.records[installation_id]
            self.change_record(installation_id, {
                "plugin_id": plugin_id,
                "current": version,
                "previous": previous["current"] if previous else None,
                "settings": previous["settings"] if previous else {},
                "account_settings": previous.get("account_settings", {}) if previous else {},
                "enabled": False,
            })
        except BaseException:
            self.discard(version)
            raise
        if previous:
            self.discard(previous["previous"])
        self.errors.pop(installation_id, None)
        return installation_id

    def activate_update(self, installation_id, package):
        """Keep the last working code and restore its complete state if activation fails."""
        old = copy.deepcopy(self.records[installation_id])
        self.pending_updates[installation_id] = old
        try:
            self.save()
        except BaseException:
            self.pending_updates.pop(installation_id)
            raise
        # install_bytes normally discards the older backup. Retain it until the
        # new version has successfully loaded and its state has been saved.
        self.records[installation_id]["previous"] = None
        try:
            self.install_bytes(package["payload"], package["metadata"], package["package_type"],
                               installation_id, trust=package["trust"])
            if old["enabled"]:
                self.enable(installation_id)
                if installation_id not in self.loaded:
                    raise RuntimeError("Обновление не запущено. Сохранена предыдущая версия.")
            self.finish_update(installation_id)
        except BaseException:
            failed = self.records[installation_id]
            if installation_id in self.loaded:
                self.unload(installation_id)
            self.change_record(installation_id, old)
            if failed["current"]["directory"] != old["current"]["directory"]:
                self.discard(failed["current"])
            if old["enabled"] and not self.restart_required:
                self.load(installation_id)
            if installation_id in self.pending_updates:
                self.finish_update(installation_id)
            raise
        try:
            self.discard(old["previous"])
        except OSError as error:
            self.logger.warning("Не удалось удалить старую резервную копию: %s", error)

    def enable(self, installation_id):
        if self.disabled or self.recovery or self.restart_required:
            raise RuntimeError("Запуск плагинов сейчас отключён.")
        if installation_id in self.loaded:
            return
        record = self.records[installation_id]
        if record["current"].get("blocked") or self.distribution.registry.cached(
                record["current"])["status"] == "blocked":
            raise ValueError("Опасный плагин / вирус: запуск запрещён.")
        requirements = record["current"]["metadata"].get("requirements", [])
        if not self.dependencies.satisfied(requirements):
            if self.dependencies.waiting_for_restart(requirements):
                self.change_record(installation_id, {**record, "enabled": True})
                self.errors[installation_id] = "Зависимости установлены. Перезапустите клиент."
                return
            self.install_dependencies(installation_id)
            return
        self.change_record(installation_id, {**record, "enabled": True})
        if not self.load(installation_id):
            self.change_record(installation_id, {**record, "enabled": False})
            raise RuntimeError(self.errors[installation_id])

    def install_dependencies(self, installation_id):
        """Resolves the requirements of every enabled plugin and this one in
        the background; the plugin starts when they are ready."""
        record = self.records[installation_id]
        requirements = set(record["current"]["metadata"].get("requirements", []))
        for other, entry in self.records.items():
            if entry["enabled"] and other != installation_id:
                requirements.update(entry["current"]["metadata"].get("requirements", []))

        def done(error):
            current = self.records.get(installation_id)
            if current is None or current["current"] is not record["current"]:
                return  # Removed or updated meanwhile.
            if error is not None:
                self.change_record(installation_id, {**current, "enabled": False})
                self.report_error(installation_id, error)
            elif not current["enabled"]:
                return  # Disabled meanwhile: the libraries stay for later.
            elif self.dependencies.satisfied(record["current"]["metadata"]["requirements"]):
                self.errors.pop(installation_id, None)
                if not (self.disabled or self.recovery or self.restart_required):
                    self.load(installation_id)
            else:
                self.errors[installation_id] = "Зависимости установлены. Перезапустите клиент."

        self.dependencies.install(installation_id, sorted(requirements), done)
        self.errors.pop(installation_id, None)
        self.change_record(installation_id, {**record, "enabled": True})

    def disable(self, installation_id):
        record = self.records[installation_id]
        self.change_record(installation_id, {**record, "enabled": False})
        self.unload(installation_id)

    def rollback(self, installation_id):
        record = self.records[installation_id]
        if not record["previous"]:
            raise ValueError("Предыдущая версия отсутствует.")
        self.check_integrity(record["previous"])
        trust = self.distribution.registry.cached(record["previous"])
        if trust["status"] == "blocked" or record["previous"].get("blocked"):
            raise ValueError("Предыдущая версия заблокирована.")
        if record["current"].get("blocked") or self.distribution.registry.cached(
                record["current"])["status"] == "revoked":
            raise ValueError("Для безопасного отката сначала проверьте обновления через сервер.")
        self.disable(installation_id)
        record = self.records[installation_id]
        self.change_record(installation_id, {
            **record, "current": record["previous"], "previous": record["current"],
            "enabled": False,
        })
        self.errors.pop(installation_id, None)

    def remove(self, installation_id, keep_data=False):
        record = self.records[installation_id]
        if keep_data:
            saved = self.root / "retained" / installation_id
            saved.mkdir(parents=True, exist_ok=True)
            (saved / "settings.json").write_text(json.dumps({
                "plugin_id": record["plugin_id"], "settings": record["settings"],
                "account_settings": record.get("account_settings", {})}, ensure_ascii=False), encoding="utf-8")
        self.disable(installation_id)
        self.change_record(installation_id, None)
        self.discard(record["current"])
        self.discard(record["previous"])
        self.errors.pop(installation_id, None)
        data = self.root / "data" / installation_id
        if not keep_data and data.is_dir() and data.resolve().parent == self.root / "data":
            shutil.rmtree(data)

    def resume(self):
        if self.disabled or self.restart_required:
            raise RuntimeError("Перезапустите клиент без режима отключения плагинов.")
        if not self.recovery:
            return
        self.recovery = False
        for installation_id, record in self.records.items():
            if record["enabled"]:
                self.load(installation_id)

    @staticmethod
    def account_key(account_id):
        result = str(account_id)
        if not result.isdecimal():
            raise ValueError("Некорректный ID аккаунта.")
        return result

    def set_setting(self, installation_id, key, value, account_id=None):
        if not isinstance(key, str) or not key or len(key) > 128:
            raise ValueError("Недопустимый ключ настройки.")
        if len(json.dumps(value, ensure_ascii=False, allow_nan=False)) > 65536:
            raise ValueError("Слишком большое значение настройки.")
        record = self.records[installation_id]
        if account_id is not None:
            account = self.account_key(account_id)
            accounts = record.get("account_settings", {})
            settings = {**accounts.get(account, {}), key: value}
            self.change_record(installation_id, {
                **record, "account_settings": {**accounts, account: settings},
            })
            return
        self.change_record(installation_id, {
            **record, "settings": {**record["settings"], key: value},
        })

    def settings(self, installation_id):
        instance, context, _ = self.loaded[installation_id]
        result = []
        keys = set()
        actions = {}
        for item in self.call(installation_id, instance.create_settings):
            if isinstance(item, Header):
                if not isinstance(item.text, str) or not item.text:
                    raise ValueError("Подраздел настроек требует непустой заголовок.")
                result.append({"kind": "header", "text": item.text})
                continue
            if (not isinstance(item, (Switch, Input, Selector, Button))
                or not isinstance(item.key, str) or not 0 < len(item.key) <= 128
                or not isinstance(item.text, str) or item.key in keys):
                raise ValueError("Некорректное описание настройки.")
            keys.add(item.key)
            value = None if isinstance(item, Button) else context.get(item.key, item.default)
            field = {"key": item.key, "text": item.text}
            if isinstance(item, Button):
                if not callable(item.on_click):
                    raise ValueError("Кнопка настроек требует обработчик нажатия.")
                previous = self.setting_actions.get((installation_id, item.key))
                token = previous["token"] if previous and previous["context"] is context else uuid.uuid4().hex
                actions[(installation_id, item.key)] = {"token": token, "context": context, "callback": item.on_click}
                field.update(kind="button", action_id=token)
            elif isinstance(item, Switch):
                field.update(kind="switch", value=bool(value))
            elif isinstance(item, Input):
                field.update(kind="input", value=str(value))
            else:
                if not item.items or not all(isinstance(text, str) for text in item.items):
                    raise ValueError("Selector требует непустой список строк.")
                index = value if type(value) is int and 0 <= value < len(item.items) else 0
                field.update(kind="selector", value=index, items=item.items)
            result.append(field)
        self.setting_actions = {key: value for key, value in self.setting_actions.items()
                                if key[0] != installation_id}
        self.setting_actions.update(actions)
        return result

    def settings_action(self, installation_id, action_id):
        action = next((entry for (identity, _), entry in self.setting_actions.items()
                       if identity == installation_id and entry["token"] == action_id), None)
        if action is None or not action["context"].active or installation_id not in self.loaded:
            raise ValueError("Кнопка настроек устарела или плагин выключен.")
        result = self.call(installation_id, action["callback"])
        if inspect.iscoroutine(result):
            self.runtime.schedule(action["context"], result)

    def save_settings(self, installation_id, values):
        fields = [field for field in self.settings(installation_id)
                  if field["kind"] in ("switch", "input", "selector")]
        if values.keys() != {field["key"] for field in fields}:
            raise ValueError("Набор настроек изменился. Откройте диалог заново.")
        for field in fields:
            value = values[field["key"]]
            if type(value) is not type(field["value"]):
                raise ValueError("Некорректный тип настройки.")
            if isinstance(value, str) and len(value) > 65536:
                raise ValueError("Слишком длинное значение настройки.")
            if field["kind"] == "selector" and not 0 <= value < len(field["items"]):
                raise ValueError("Некорректное значение списка.")
        record = self.records[installation_id]
        self.change_record(installation_id, {**record, "settings": {**record["settings"], **values}})

    def describe(self, installation_id):
        record = self.records[installation_id]
        version = record["current"]
        trust = self.distribution.registry.cached(version)
        author_hidden = protected_author(version["metadata"]["author"], trust["status"])
        return {**version["metadata"], "installation_id": installation_id,
                "trust": trust, "display_author": "Неизвестный автор" if author_hidden else version["metadata"]["author"],
                "author_hidden": author_hidden,
                "previously_trusted": version.get("trust", {}).get("status") in TRUSTED,
                "update": self.distribution.offers.get(installation_id),
                "plugin_id": record["plugin_id"], "enabled": record["enabled"],
                "sha256": version.get("sha256"), "package_type": version.get("package_type"),
                "legacy": version.get("format") == "legacy"}

    def snapshot(self):
        dependencies = self.dependencies.status()
        return {
            "sdk_version": SDK_VERSION,
            "disabled": self.disabled,
            "recovery": self.recovery,
            "restart_required": self.restart_required,
            "log_path": str(self.root / "plugins.log"),
            "dependencies": dependencies,
            "distribution": self.distribution.status(),
            "plugins": [
                {**self.describe(installation_id),
                 "installing": dependencies["installing"] == installation_id,
                 "loaded": installation_id in self.loaded,
                 "previous": record["previous"] is not None,
                 "instances": len(self.installations_of(record["plugin_id"])),
                 "error": self.errors.get(installation_id, "")}
                for installation_id, record in sorted(
                    self.records.items(), key=lambda item: (item[1]["plugin_id"], item[0]))
            ],
        }

    def dispatch(self, request):
        self.check_thread()
        action = json.loads(request)
        name = action.pop("action")
        if name in ("snapshot", "poll", "client_event", "ui_event"):
            # A finished dependency installation starts its plugin here, on
            # the main thread and outside of any hook.
            self.dependencies.poll()
            self.distribution.poll()
        allowed = {
            "poll": self.poll_distribution,
            "prepare_install": self.distribution.prepare,
            "prepared_install": self.distribution.prepared,
            "commit_install": self.distribution.commit,
            "discard_install": self.distribution.discard,
            "check_updates": lambda: self.distribution.start_check(manual=True),
            "apply_update": self.distribution.apply_offer,
            "snapshot": self.snapshot, "inspect": self.inspect, "install": self.install,
            "enable": self.enable,
            "disable": self.disable, "rollback": self.rollback, "remove": self.remove,
            "resume": self.resume, "settings": self.settings, "save_settings": self.save_settings,
            "settings_action": self.settings_action,
            "share_file": self.share_file,
            "client_reply": self.runtime.complete,
            "client_pending": self.runtime.is_pending,
            "bridge_ready": lambda: self.runtime.ready.set(),
            "native_hook": self.runtime.native_hook,
            "client_event": self.runtime.native_event,
            "ui_execute": self.runtime.execute_ui,
            "ui_event": self.runtime.ui_event,
        }
        try:
            return json.dumps({"result": allowed[name](**action)}, ensure_ascii=False)
        except HookCancelled as error:
            return json.dumps({"error": str(error), "cancelled": True}, ensure_ascii=False)
        except BaseException as error:
            installation_id = action.get("installation_id", "")
            message = str(error) or type(error).__name__
            if installation_id in self.records and installation_id not in self.errors:
                self.report_error(installation_id, message)
            else:
                self.logger.exception("%s: %s", name, message)
            return json.dumps({"error": message}, ensure_ascii=False)

    def shutdown(self):
        self.check_thread()
        self.distribution.close()
        for installation_id in reversed(tuple(self.loaded)):
            try:
                self.unload(installation_id)
            except RuntimeError:
                pass
        self.runtime.stop()
        # The marker detects crashes: a clean exit removes it, also after a
        # failed unload. Recovery mode and --disable-plugins keep it, so the
        # next start still asks before loading plugins.
        if not (self.recovery or self.disabled):
            self.marker.unlink(missing_ok=True)
        self.log_handler.close()

    def poll_distribution(self):
        self.distribution.start_check()
        self.distribution.poll()
        notices, self.distribution.notices = self.distribution.notices, []
        return notices
