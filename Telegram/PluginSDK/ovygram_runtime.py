"""The process-wide Python side of the desktop plugin host."""

import ast
import copy
import importlib.util
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
from ui.settings import Input, Selector, Switch


SDK_VERSION = 2
MAX_PACKAGE = 32 * 1024 * 1024
MAX_SOURCE = 1024 * 1024
PLUGIN_ID = re.compile(r"[a-z][a-z0-9_.-]{0,63}\Z")
VERSION_DIR = re.compile(r"[0-9a-f]{32}\Z")
METADATA = {
    "__id__": "id", "__name__": "name", "__version__": "version",
    "__author__": "author", "__description__": "description",
    "__platform__": "platform", "__desktop_sdk__": "sdk",
    "__requirements__": "requirements",
}


def read_metadata(source, filename):
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
            if isinstance(target, ast.Name) and target.id in METADATA:
                key = METADATA[target.id]
                if key in values:
                    raise ValueError(f"Метаданные {target.id} указаны дважды.")
                values[key] = ast.literal_eval(node.value)
    for key in ("id", "name", "version", "author", "description"):
        if not isinstance(values.get(key), str) or not values[key].strip():
            raise ValueError(f"Укажите строковое поле {key} в метаданных.")
    if not PLUGIN_ID.fullmatch(values["id"]):
        raise ValueError("Недопустимый ID плагина.")
    if values.get("platform") != "desktop":
        raise ValueError('Укажите __platform__ = "desktop". Android-плагины требуют переноса.')
    if type(values.get("sdk")) is not int or not 1 <= values["sdk"] <= SDK_VERSION:
        raise ValueError(f"Поддерживаются версии Desktop SDK от 1 до {SDK_VERSION}.")
    if values.get("requirements", []) != []:
        raise ValueError("Установка сторонних зависимостей пока недоступна.")
    return values


def package_path(name):
    path = PurePosixPath(name)
    parts = name.rstrip("/").split("/")
    if any(not part or part in (".", "..") or part[-1] in " ."
           or re.search(r'[\\:<>"|?*\x00-\x1f]', part)
           or part.split(".")[0].rstrip(" ").upper() in {
               "CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$",
               *(f"COM{i}" for i in "123456789¹²³"),
               *(f"LPT{i}" for i in "123456789¹²³"),
           } for part in parts):
        raise ValueError("Недопустимый путь внутри ZIP.")
    return path


def unpack_package(source, target):
    if source.suffix.lower() in (".py", ".plugin"):
        with source.open("rb") as stream:
            content = stream.read(MAX_SOURCE + 1)
        metadata = read_metadata(content, str(source))
        (target / "plugin.py").write_bytes(content)
        return metadata, "plugin.py"
    if source.suffix.lower() != ".zip":
        raise ValueError("Выберите файл .py, .plugin или .zip.")
    if source.stat().st_size > MAX_PACKAGE:
        raise ValueError("Архив плагина больше 32 МиБ.")
    with zipfile.ZipFile(source) as archive:
        entries = archive.infolist()
        if len(entries) > 512 or sum(entry.file_size for entry in entries) > MAX_PACKAGE:
            raise ValueError("Слишком много файлов или распакованных данных.")
        files = {}
        paths = set()
        for entry in entries:
            path = package_path(entry.orig_filename)
            folded = path.as_posix().casefold()
            if folded in paths or (entry.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("ZIP содержит повторный путь или символьную ссылку.")
            paths.add(folded)
            if not entry.is_dir():
                files[path.as_posix()] = entry
        manifest = files.get("plugin.json")
        if manifest is None or manifest.file_size > 4096:
            raise ValueError("Добавьте в корень ZIP файл plugin.json с полем entry.")
        entry = json.loads(archive.read(manifest))["entry"]
        if not isinstance(entry, str):
            raise ValueError("Поле entry должно быть строкой.")
        main = package_path(entry)
        if len(main.parts) != 1 or main.suffix.lower() not in (".py", ".plugin"):
            raise ValueError("Точка входа должна быть файлом .py или .plugin в корне ZIP.")
        if entry not in files or files[entry].file_size > MAX_SOURCE:
            raise ValueError("Точка входа отсутствует или больше 1 МиБ.")
        metadata = read_metadata(archive.read(files[entry]), entry)
        for name, member in files.items():
            destination = target.joinpath(*PurePosixPath(name).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as reader, destination.open("xb") as writer:
                shutil.copyfileobj(reader, writer)
        return metadata, entry


class PluginContext:
    def __init__(self, manager, plugin_id):
        self.manager = manager
        self.plugin_id = plugin_id
        self.active = True

    def get(self, key, default, account_id=None):
        self.check_active()
        record = self.manager.records[self.plugin_id]
        settings = record["settings"] if account_id is None else record.get(
            "account_settings", {}).get(self.manager.account_key(account_id), {})
        return copy.deepcopy(settings.get(key, default))

    def set(self, key, value, account_id=None):
        self.check_active()
        self.manager.check_thread()
        self.manager.set_setting(self.plugin_id, key, value, account_id)

    def log(self, message):
        self.check_active()
        self.manager.logger.info("%s: %s", self.plugin_id, message)

    def check_active(self):
        if not self.active:
            raise RuntimeError("Плагин уже выгружен.")


class Manager:
    def __init__(self, root, disabled=False):
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
        self.logger = logging.Logger("ovygram")
        self.log_handler = RotatingFileHandler(
            self.root / "plugins.log", maxBytes=1024 * 1024, backupCount=2,
            encoding="utf-8",
        )
        self.log_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        self.logger.addHandler(self.log_handler)
        self.runtime = Runtime(self)
        self.records = json.loads(self.state.read_text(encoding="utf-8")) if self.state.exists() else {}
        if not isinstance(self.records, dict) or any(
            not PLUGIN_ID.fullmatch(plugin_id) or not isinstance(record, dict)
            or not {"current", "previous", "enabled", "settings"} <= record.keys()
            for plugin_id, record in self.records.items()
        ):
            raise ValueError("Повреждён файл состояния плагинов.")
        if not (self.disabled or self.recovery):
            for plugin_id, record in self.records.items():
                if record["enabled"]:
                    self.load(plugin_id)

    def check_thread(self):
        if threading.get_ident() != self.owner:
            raise RuntimeError("Настройки плагина доступны только в главном потоке.")

    def save(self):
        text = json.dumps(self.records, ensure_ascii=False, allow_nan=False, indent=2)
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

    def report_error(self, plugin_id, message):
        self.errors[plugin_id] = message
        self.logger.exception("%s: %s", plugin_id, message)

    def call(self, plugin_id, method, *args):
        return self.runtime.call(self.runtime.contexts[plugin_id], method, *args)

    def load(self, plugin_id):
        record = self.records[plugin_id]
        version = record["current"]
        namespace = "_ovygram_" + version["directory"]
        context = PluginContext(self, plugin_id)
        self.runtime.contexts[plugin_id] = context
        self.marker.write_text(plugin_id, encoding="utf-8")
        try:
            directory = self.directory(version)
            entry = version["entry"]
            if len(package_path(entry).parts) != 1:
                raise ValueError("Недопустимая точка входа.")
            path = directory / entry
            if path.resolve().parent != directory:
                raise ValueError("Точка входа выходит за пределы каталога плагина.")
            spec = importlib.util.spec_from_loader(namespace, loader=None, is_package=True)
            module = importlib.util.module_from_spec(spec)
            module.__file__ = str(path)
            module.__path__ = [str(directory)]
            sys.modules[namespace] = module
            with path.open("rb") as stream:
                source = stream.read(MAX_SOURCE + 1)
            if read_metadata(source, str(path)) != version["metadata"]:
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
            self.call(plugin_id, instance.on_plugin_load)
            self.loaded[plugin_id] = (instance, context, namespace)
            self.errors.pop(plugin_id, None)
            return True
        except BaseException as error:
            context.active = False
            self.runtime.remove(plugin_id)
            self.clear_modules(namespace)
            message = str(error) or type(error).__name__
            if isinstance(error, ModuleNotFoundError) and (error.name or "").split(".")[0] in {
                "android", "java", "jnius", "chaquopy", "org",
            }:
                message = "Этот импорт относится к Android. Адаптируйте плагин для Desktop SDK."
            self.report_error(plugin_id, message)
            return False

    @staticmethod
    def clear_modules(namespace):
        for name in tuple(sys.modules):
            if name == namespace or name.startswith(namespace + "."):
                sys.modules.pop(name, None)

    def unload(self, plugin_id):
        if plugin_id not in self.loaded:
            return
        instance, context, namespace = self.loaded.pop(plugin_id)
        try:
            self.call(plugin_id, instance.on_plugin_unload)
        except BaseException as error:
            self.restart_required = True
            self.report_error(plugin_id, str(error) or type(error).__name__)
            raise RuntimeError("Выгрузка завершилась ошибкой. Перезапустите клиент.") from error
        finally:
            context.active = False
            self.runtime.remove(plugin_id)
            self.clear_modules(namespace)

    def change_record(self, plugin_id, record):
        previous = self.records.get(plugin_id)
        if record is None:
            del self.records[plugin_id]
        else:
            self.records[plugin_id] = record
        try:
            self.save()
        except BaseException:
            if previous is None:
                self.records.pop(plugin_id, None)
            else:
                self.records[plugin_id] = previous
            raise

    def install(self, path, plugin_id=""):
        token = uuid.uuid4().hex
        version = {"directory": token}
        directory = self.directory(version)
        directory.mkdir()
        try:
            metadata, entry = unpack_package(Path(path), directory)
            version.update(metadata=metadata, entry=entry)
            if plugin_id and plugin_id != metadata["id"]:
                raise ValueError("ID обновления отличается от ID установленного плагина.")
            previous = self.records.get(metadata["id"])
            if previous and not plugin_id:
                raise ValueError("Плагин уже установлен. Используйте обновление из файла.")
            plugin_id = metadata["id"]
            if previous:
                self.unload(plugin_id)
                previous = self.records[plugin_id]
            self.change_record(plugin_id, {
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
        self.errors.pop(plugin_id, None)
        return plugin_id

    def enable(self, plugin_id):
        if self.disabled or self.recovery or self.restart_required:
            raise RuntimeError("Запуск плагинов сейчас отключён.")
        if plugin_id in self.loaded:
            return
        record = self.records[plugin_id]
        self.change_record(plugin_id, {**record, "enabled": True})
        if not self.load(plugin_id):
            self.change_record(plugin_id, {**record, "enabled": False})
            raise RuntimeError(self.errors[plugin_id])

    def disable(self, plugin_id):
        record = self.records[plugin_id]
        self.change_record(plugin_id, {**record, "enabled": False})
        self.unload(plugin_id)

    def rollback(self, plugin_id):
        record = self.records[plugin_id]
        if not record["previous"]:
            raise ValueError("Предыдущая версия отсутствует.")
        self.disable(plugin_id)
        record = self.records[plugin_id]
        self.change_record(plugin_id, {
            **record, "current": record["previous"], "previous": record["current"],
            "enabled": False,
        })
        self.errors.pop(plugin_id, None)

    def remove(self, plugin_id):
        record = self.records[plugin_id]
        self.disable(plugin_id)
        self.change_record(plugin_id, None)
        self.discard(record["current"])
        self.discard(record["previous"])
        self.errors.pop(plugin_id, None)

    def resume(self):
        if self.disabled or self.restart_required:
            raise RuntimeError("Перезапустите клиент без режима отключения плагинов.")
        if not self.recovery:
            return
        self.recovery = False
        for plugin_id, record in self.records.items():
            if record["enabled"]:
                self.load(plugin_id)

    @staticmethod
    def account_key(account_id):
        result = str(account_id)
        if not result.isdecimal():
            raise ValueError("Некорректный ID аккаунта.")
        return result

    def set_setting(self, plugin_id, key, value, account_id=None):
        if not isinstance(key, str) or not key or len(key) > 128:
            raise ValueError("Недопустимый ключ настройки.")
        if len(json.dumps(value, ensure_ascii=False, allow_nan=False)) > 65536:
            raise ValueError("Слишком большое значение настройки.")
        record = self.records[plugin_id]
        if account_id is not None:
            account = self.account_key(account_id)
            accounts = record.get("account_settings", {})
            settings = {**accounts.get(account, {}), key: value}
            self.change_record(plugin_id, {
                **record, "account_settings": {**accounts, account: settings},
            })
            return
        self.change_record(plugin_id, {
            **record, "settings": {**record["settings"], key: value},
        })

    def settings(self, plugin_id):
        instance, context, _ = self.loaded[plugin_id]
        result = []
        keys = set()
        for item in self.call(plugin_id, instance.create_settings):
            if (not isinstance(item, (Switch, Input, Selector))
                or not isinstance(item.key, str) or not 0 < len(item.key) <= 128
                or not isinstance(item.text, str) or item.key in keys):
                raise ValueError("Некорректное описание настройки.")
            keys.add(item.key)
            value = context.get(item.key, item.default)
            field = {"key": item.key, "text": item.text}
            if isinstance(item, Switch):
                field.update(kind="switch", value=bool(value))
            elif isinstance(item, Input):
                field.update(kind="input", value=str(value))
            else:
                if not item.items or not all(isinstance(text, str) for text in item.items):
                    raise ValueError("Selector требует непустой список строк.")
                index = value if type(value) is int and 0 <= value < len(item.items) else 0
                field.update(kind="selector", value=index, items=item.items)
            result.append(field)
        return result

    def save_settings(self, plugin_id, values):
        fields = self.settings(plugin_id)
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
        record = self.records[plugin_id]
        self.change_record(plugin_id, {**record, "settings": {**record["settings"], **values}})

    def snapshot(self):
        return {
            "sdk_version": SDK_VERSION,
            "disabled": self.disabled,
            "recovery": self.recovery,
            "restart_required": self.restart_required,
            "log_path": str(self.root / "plugins.log"),
            "plugins": [
                {**record["current"]["metadata"], "enabled": record["enabled"],
                 "loaded": plugin_id in self.loaded, "previous": record["previous"] is not None,
                 "error": self.errors.get(plugin_id, "")}
                for plugin_id, record in sorted(self.records.items())
            ],
        }

    def dispatch(self, request):
        self.check_thread()
        action = json.loads(request)
        name = action.pop("action")
        allowed = {
            "snapshot": self.snapshot, "install": self.install, "enable": self.enable,
            "disable": self.disable, "rollback": self.rollback, "remove": self.remove,
            "resume": self.resume, "settings": self.settings, "save_settings": self.save_settings,
            "client_reply": self.runtime.complete,
            "client_pending": self.runtime.is_pending,
            "bridge_ready": lambda: self.runtime.ready.set(),
            "native_hook": self.runtime.native_hook,
            "client_event": self.runtime.native_event,
            "ui_execute": self.runtime.execute_ui,
        }
        try:
            return json.dumps({"result": allowed[name](**action)}, ensure_ascii=False)
        except HookCancelled as error:
            return json.dumps({"error": str(error), "cancelled": True}, ensure_ascii=False)
        except BaseException as error:
            plugin_id = action.get("plugin_id", "")
            message = str(error) or type(error).__name__
            if plugin_id in self.records and plugin_id not in self.errors:
                self.report_error(plugin_id, message)
            else:
                self.logger.exception("%s: %s", name, message)
            return json.dumps({"error": message}, ensure_ascii=False)

    def shutdown(self):
        self.check_thread()
        for plugin_id in reversed(tuple(self.loaded)):
            try:
                self.unload(plugin_id)
            except RuntimeError:
                pass
        self.runtime.stop()
        if not (self.recovery or self.disabled or self.restart_required):
            self.marker.unlink(missing_ok=True)
        self.log_handler.close()
