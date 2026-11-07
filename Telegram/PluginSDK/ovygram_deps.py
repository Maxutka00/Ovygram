"""Third-party libraries of plugins.

All plugins share one environment: a directory pip installs into with
--target, appended to sys.path. Its packages are resolved together from the
requirements of every enabled plugin, so a version conflict is reported by
pip's resolver instead of one plugin silently replacing another's library.

pip runs in a separate process from the bundled pip wheel and installs only
wheels: pure Python ones and binary ones for this platform, nothing is
compiled on the user's machine. Each resolution goes into a new directory.
If it keeps the versions of the packages already in use, it is activated at
once; otherwise it is activated on the next start, because loaded modules,
native ones especially, can't be replaced in a running process.
"""

from concurrent.futures import Future
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import threading
import uuid

MAX_REQUIREMENTS = 32
MAX_REQUIREMENT = 200
INSTALL_TIMEOUT = 15 * 60
ERROR_LINES = 12

_VERSION = r"[A-Za-z0-9.*+!_-]+"
_CLAUSE = rf"(==|!=|<=|>=|~=|<|>)\s*{_VERSION}"
# A name, optional extras and version clauses. No URLs, paths, markers or
# options: a requirement can't make pip do anything but pick a version.
REQUIREMENT = re.compile(
    rf"(?P<name>[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?)\s*"
    rf"(?P<extras>\[\s*[A-Za-z0-9._-]+(?:\s*,\s*[A-Za-z0-9._-]+)*\s*\])?\s*"
    rf"(?P<spec>{_CLAUSE}(?:\s*,\s*{_CLAUSE})*)?\Z")


class DependencyError(RuntimeError):
    pass


def normalize_name(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def normalize(requirement):
    """The canonical form of one requirement, e.g. "Requests >= 2" ->
    "requests>=2". Raises ValueError for anything but name, extras and
    version clauses."""
    if not isinstance(requirement, str) or len(requirement) > MAX_REQUIREMENT:
        raise ValueError("Зависимость задаётся строкой до 200 символов.")
    match = REQUIREMENT.fullmatch(requirement.strip())
    if match is None:
        raise ValueError(
            f"Неподдерживаемая зависимость {requirement!r}: укажите имя пакета и "
            "версию, например \"requests>=2.31\".")
    result = normalize_name(match["name"])
    if match["extras"]:
        extras = sorted(normalize_name(item.strip())
                        for item in match["extras"].strip("[] ").split(","))
        result += "[" + ",".join(extras) + "]"
    if match["spec"]:
        result += re.sub(r"\s+", "", match["spec"])
    return result


def normalize_all(requirements):
    if not isinstance(requirements, list):
        raise ValueError("__requirements__ должен быть списком строк.")
    if len(requirements) > MAX_REQUIREMENTS:
        raise ValueError(f"Не больше {MAX_REQUIREMENTS} зависимостей.")
    return sorted({normalize(item) for item in requirements})


def default_runner(command, environment, log_path):
    """Runs pip and returns (exit code, output)."""
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        result = subprocess.run(
            command, env=environment, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=INSTALL_TIMEOUT, creationflags=flags)
    except subprocess.TimeoutExpired as error:
        output = (error.output or b"").decode("utf-8", "replace")
        log_path.write_text(output, encoding="utf-8")
        raise DependencyError("Установка зависимостей не уложилась в 15 минут.") from error
    output = result.stdout.decode("utf-8", "replace")
    log_path.write_text(output, encoding="utf-8")
    return result.returncode, output


class Dependencies:
    def __init__(self, root, python_dir, runner=default_runner):
        self.root = Path(root) / "dependencies"
        self.root.mkdir(parents=True, exist_ok=True)
        self.state_path = Path(root) / "dependencies.json"
        self.python_dir = Path(python_dir)
        self.runner = runner
        self.lock = threading.Lock()
        self.job = None  # (Future, plugin ID, requirements)
        self.state = {"active": None, "pending": None, "requirements": [], "packages": {},
                      "pending_requirements": [], "pending_packages": {}}
        if self.state_path.exists():
            loaded = json.loads(self.state_path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                self.state.update(loaded)
        self.start()

    # Startup.

    def start(self):
        """Activates a resolution waiting for the restart, removes the
        directories nothing uses and puts the active one on sys.path."""
        pending = self.state.get("pending")
        if pending and (self.root / pending).is_dir():
            self.state.update(active=pending, requirements=self.state["pending_requirements"],
                              packages=self.state["pending_packages"])
        self.state.update(pending=None, pending_requirements=[], pending_packages={})
        active = self.state.get("active")
        if active and not (self.root / active).is_dir():
            self.state.update(active=None, requirements=[], packages={})
            active = None
        for child in self.root.iterdir():
            if child.is_dir() and child.name != active:
                shutil.rmtree(child, ignore_errors=True)
        self.save()
        if active:
            self.add_to_path(self.root / active)

    def save(self):
        temporary = self.state_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(self.state, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(self.state_path)

    @staticmethod
    def add_to_path(directory, replace=None):
        path = str(directory)
        if replace is not None and str(replace) in sys.path:
            sys.path[sys.path.index(str(replace))] = path
        elif path not in sys.path:
            # After the standard library and the SDK, so a plugin library
            # can't shadow them.
            sys.path.append(path)
        importlib.invalidate_caches()

    # Queries.

    def satisfied(self, requirements):
        return set(requirements) <= set(self.state["requirements"])

    def waiting_for_restart(self, requirements):
        return bool(self.state.get("pending")) and set(requirements) <= set(
            self.state["pending_requirements"])

    def installing(self):
        with self.lock:
            return self.job is not None and not self.job[0].done()

    def status(self):
        with self.lock:
            job = self.job
        return {
            "installing": job[1] if job is not None and not job[0].done() else "",
            "restart": bool(self.state.get("pending")),
            "packages": dict(sorted(self.state["packages"].items())),
        }

    # Installation.

    def interpreter(self):
        """The command and environment that run Python with pip."""
        pip = self.python_dir / "pip.whl"
        if not pip.is_file():
            raise DependencyError("В этой сборке нет pip для установки зависимостей.")
        environment = {key: value for key, value in os.environ.items()
                       if not key.startswith("PYTHON")}
        environment.update(PYTHONNOUSERSITE="1", PYTHONUTF8="1", PIP_NO_INPUT="1")
        executable = self.python_dir / ("python.exe" if os.name == "nt" else "python")
        stdlib = self.python_dir / "python313.zip"
        if executable.is_file() and stdlib.is_file():
            # The bundled interpreter finds its library only through these.
            environment.update(PYTHONHOME=str(self.python_dir), PYTHONPATH=os.pathsep.join(
                (str(stdlib), str(self.python_dir))))
            python = str(executable)
        else:
            version = f"{sys.version_info.major}.{sys.version_info.minor}"
            python = shutil.which(f"python{version}") or shutil.which("python3")
            if python is None:
                raise DependencyError(f"Не найден системный Python {version}.")
        # pip runs from its wheel, the documented way to use a pip wheel.
        return [python, str(pip / "pip")], environment

    def install(self, plugin_id, requirements, done):
        """Resolves requirements (of every enabled plugin) in the background.
        done(error) is called later from poll() on the main thread; error is
        None or a message for the user."""
        with self.lock:
            if self.job is not None and not self.job[0].done():
                raise DependencyError(
                    f"Уже устанавливаются зависимости плагина {self.job[1]}. Подождите.")
            command, environment = self.interpreter()
            future = Future()
            self.job = (future, plugin_id, list(requirements), done)
        thread = threading.Thread(
            target=self.run, args=(future, command, environment, list(requirements)),
            name="Ovygram dependencies", daemon=True)
        thread.start()

    def run(self, future, command, environment, requirements):
        target = self.root / uuid.uuid4().hex
        try:
            target.mkdir()
            code, output = self.runner([
                *command, "install", "--target", str(target),
                "--only-binary=:all:", "--no-input", "--disable-pip-version-check",
                "--no-warn-script-location", "--progress-bar", "off",
                "--", *requirements,
            ], environment, self.root / "install.log")
            if code != 0:
                raise DependencyError(self.explain(output))
            packages = {
                normalize_name(item.metadata["Name"]): item.version
                for item in importlib.metadata.distributions(path=[str(target)])
            }
            future.set_result((target, packages))
        except BaseException as error:
            shutil.rmtree(target, ignore_errors=True)
            future.set_exception(error)

    @staticmethod
    def explain(output):
        lines = [line.rstrip() for line in output.splitlines() if line.strip()]
        errors = [line for line in lines if line.startswith("ERROR:")] or lines[-ERROR_LINES:]
        text = "\n".join(errors[-ERROR_LINES:]) or "pip завершился с ошибкой."
        return "Не удалось установить зависимости:\n" + text

    def poll(self):
        """Applies a finished installation; call on the main thread."""
        with self.lock:
            if self.job is None or not self.job[0].done():
                return
            future, plugin_id, requirements, done = self.job
            self.job = None
        try:
            target, packages = future.result()
        except BaseException as error:
            done(str(error) or type(error).__name__)
            return
        current = self.state["packages"]
        live = all(packages.get(name) == version for name, version in current.items())
        if live:
            previous = self.state.get("active")
            self.state.update(active=target.name, requirements=requirements, packages=packages,
                              pending=None, pending_requirements=[], pending_packages={})
            self.save()
            self.add_to_path(target, replace=self.root / previous if previous else None)
        else:
            self.state.update(pending=target.name, pending_requirements=requirements,
                              pending_packages=packages)
            self.save()
        done(None)
