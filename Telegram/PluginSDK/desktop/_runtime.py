"""Plugin-owned subscriptions, tasks and the asynchronous native boundary."""

import asyncio
from collections import OrderedDict
import base64
from concurrent.futures import Future, InvalidStateError
import contextvars
import copy
import hashlib
from dataclasses import dataclass
import inspect
import json
import sys
import threading
import time
import uuid

from hook_utils import CANCEL, DEFAULT, MODIFY, MODIFY_FINAL, HookCancelled, HookError, HookResult
from . import tl


_current = contextvars.ContextVar("desktop_plugin_context", default=None)
_hook_stack = contextvars.ContextVar("desktop_hook_stack", default=())
# Requests before_send hooks see, besides before_rpc.
OUTGOING = frozenset({
    "messages.sendMessage", "messages.sendMedia", "messages.sendMultiMedia",
    "messages.forwardMessages", "messages.sendInlineBotResult"})
POINT_BITS = {name: 1 << index for index, name in enumerate((
    "before_send", "before_rpc", "after_rpc", "before_updates", "new_message",
    "edited_message", "deleted_message", "account_changed", "accounts_changed", "chat_changed"))}


def context():
    result = _current.get()
    if result is None or not result.active:
        raise RuntimeError("Вызов SDK должен принадлежать включённому плагину.")
    return result


class RpcError(RuntimeError):
    def __init__(self, code, name, description=""):
        self.code = code
        self.name = name
        self.description = description
        super().__init__(f"{name}: {description}" if description else name)


@dataclass
class RpcContext:
    account_id: str
    request_id: int
    request: tl.TLObject


@dataclass
class OutgoingMessage:
    account_id: str
    request: tl.TLObject

    @property
    def text(self):
        return getattr(self.request, "message", None)

    @text.setter
    def text(self, value):
        if not isinstance(value, str) or not hasattr(self.request, "message"):
            raise TypeError("Текст сообщения должен быть строкой.")
        self.request.message = value
        if hasattr(self.request, "entities"):
            self.request.entities = None


@dataclass
class RpcResponse:
    account_id: str
    request_id: int
    response: bytes | None = None
    error: dict | None = None
    request: tl.TLObject | None = None


@dataclass
class UpdateContext:
    account_id: str
    updates: tl.TLObject


@dataclass
class Registration:
    runtime: object
    installation_id: str
    point: str
    callback: object
    priority: int
    sequence: int
    request: str | None = None
    active: bool = True

    def cancel(self):
        self.active = False
        self.runtime.refresh_mask()


class Runtime:
    def __init__(self, manager):
        self.manager = manager
        self.contexts = {}
        self.registrations = []
        self.lock = threading.RLock()
        self.requests = {}
        self.tasks = {}
        self.ui_calls = {}
        self.surfaces = {}
        self.element_handlers = {}
        self.widget_rules = {}
        self.sequence = 0
        self.loop = None
        self.thread = None
        self.ready = threading.Event()
        self.stopping = False
        self.sender = None
        self.seen_events = OrderedDict()
        self.seen_messages = OrderedDict()
        self.hook_mask = 0

    def call(self, plugin_context, method, *arguments):
        if not plugin_context.active:
            raise RuntimeError("Плагин уже выгружен.")
        token = _current.set(plugin_context)
        started = time.monotonic()
        try:
            return method(*arguments)
        finally:
            _current.reset(token)
            elapsed = time.monotonic() - started
            if elapsed >= 0.1:
                self.manager.logger.warning("%s: %s %.3f s", plugin_context.installation_id,
                                            getattr(method, "__name__", "handler"), elapsed)

    def register(self, plugin_context, point, callback, priority=0, request=None):
        if not plugin_context.active or not callable(callback):
            raise ValueError("Обработчик должен принадлежать включённому плагину.")
        if point not in POINT_BITS or type(priority) is not int:
            raise ValueError("Неизвестное событие или некорректный приоритет.")
        self.sequence += 1
        registration = Registration(self, plugin_context.installation_id, point, callback,
                                    priority, self.sequence, request)
        self.registrations.append(registration)
        self.refresh_mask()
        return registration

    def refresh_mask(self):
        mask = 0
        for entry in self.registrations:
            if entry.active:
                mask |= POINT_BITS[entry.point]
        self.hook_mask = mask

    def handlers(self, point):
        return sorted((entry for entry in self.registrations if entry.active and entry.point == point),
                      key=lambda entry: (-entry.priority, self.plugin_id_of(entry.installation_id),
                                         entry.installation_id, entry.sequence))

    def plugin_id_of(self, installation_id):
        owner = self.contexts.get(installation_id)
        return owner.plugin_id if owner is not None else ""

    def hooks(self, point, value, validate, inherited=()):
        original = copy.deepcopy(value)
        current = copy.deepcopy(value)
        modified = False
        stack = (*_hook_stack.get(), *inherited)
        for handler in self.handlers(point):
            owner = self.contexts.get(handler.installation_id)
            if not handler.active or owner is None or not owner.active or handler.installation_id in stack:
                continue
            request = getattr(current, "request", None)
            if handler.request and (request is None or request.constructor_name != handler.request):
                continue
            token = _hook_stack.set((*stack, handler.installation_id))
            try:
                result = self.call(owner, handler.callback, copy.deepcopy(current))
                if inspect.isawaitable(result):
                    if inspect.iscoroutine(result):
                        result.close()
                    raise HookError("Синхронный хук не может возвращать coroutine.")
                if result is None:
                    result = HookResult()
                if not isinstance(result, HookResult) or not isinstance(result.strategy, type(DEFAULT)):
                    raise HookError("Хук должен вернуть HookResult.")
                if result.strategy == CANCEL:
                    raise HookCancelled(result.reason or "Операция отменена плагином.")
                if result.strategy in (MODIFY, MODIFY_FINAL):
                    validate(result.value, original)
                    current = copy.deepcopy(result.value)
                    modified = True
                elif result.value is not None:
                    raise HookError("DEFAULT не принимает изменённое значение.")
                if result.strategy == MODIFY_FINAL:
                    break
            except BaseException as error:
                if not isinstance(error, HookCancelled):
                    self.manager.report_error(handler.installation_id, str(error))
                if isinstance(error, HookError):
                    raise
                raise HookError(f"Ошибка хука {handler.installation_id}: {error}") from error
            finally:
                _hook_stack.reset(token)
        if modified:
            # Unchanged values aren't validated: for after_rpc that would
            # decode every response, and fail on any the codec can't read.
            validate(current, original)
        return current

    def wanted(self, point, name):
        """Whether a hook of the point handles a request of this TL name."""
        return any(not handler.request or handler.request == name
                   for handler in self.handlers(point))

    @staticmethod
    def function_name(data):
        from .tl.codec import _by_id
        declaration = _by_id.get(int.from_bytes(data[:4], "little")) if len(data) >= 4 else None
        if declaration is None or not declaration._tl["function"]:
            return None
        return declaration._tl["name"]

    def ensure_loop(self):
        with self.lock:
            if self.stopping:
                raise RuntimeError("Система плагинов завершает работу.")
            if self.loop is None:
                self.loop = asyncio.new_event_loop()
                self.thread = threading.Thread(target=self.run_loop, name="Ovygram asyncio", daemon=True)
                self.thread.start()
            return self.loop

    def run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
        self.loop.close()

    def schedule(self, plugin_context, coroutine):
        if not plugin_context.active or not inspect.iscoroutine(coroutine):
            if inspect.iscoroutine(coroutine):
                coroutine.close()
            raise ValueError("Ожидается coroutine включённого плагина.")
        try:
            loop = self.ensure_loop()
        except BaseException:
            coroutine.close()
            raise

        async def managed():
            token = _current.set(plugin_context)
            try:
                if not plugin_context.active:
                    coroutine.close()
                    return
                return await coroutine
            except asyncio.CancelledError:
                raise
            except BaseException as error:
                self.manager.report_error(plugin_context.installation_id, str(error))
                raise
            finally:
                _current.reset(token)

        future = asyncio.run_coroutine_threadsafe(managed(), loop)
        with self.lock:
            self.tasks.setdefault(plugin_context.installation_id, set()).add(future)
        future.add_done_callback(lambda done: self.task_finished(plugin_context.installation_id, done))
        return future

    def task_finished(self, installation_id, future):
        with self.lock:
            self.tasks.get(installation_id, set()).discard(future)

    def submit(self, command):
        if self.sender is not None:
            self.sender(command)
            return
        try:
            import _ovygram_native
            _ovygram_native.submit(json.dumps(command, ensure_ascii=False))
        except ImportError as error:
            raise RuntimeError("Telegram API доступен внутри Ovygram.") from error

    async def request(self, method, account_id=None, **parameters):
        owner = context()
        deadline = time.monotonic() + 15
        while not self.ready.is_set() and owner.active and time.monotonic() < deadline:
            await asyncio.sleep(0.02)
        if not self.ready.is_set() or not owner.active:
            raise RuntimeError("Мост к клиенту ещё не готов или плагин выгружен.")
        identity = uuid.uuid4().hex
        future = Future()
        command = {"id": identity, "installation_id": owner.installation_id, "method": method,
                   "account_id": account_id, "hook_stack": list(_hook_stack.get()), **parameters}
        with self.lock:
            self.requests[identity] = (owner, future)
        try:
            self.submit(command)
            return await asyncio.wrap_future(future)
        except asyncio.CancelledError:
            try:
                self.submit({"method": "cancel", "id": identity, "installation_id": owner.installation_id})
            except RuntimeError:
                pass
            raise
        finally:
            with self.lock:
                self.requests.pop(identity, None)

    def is_pending(self, request_id, installation_id):
        with self.lock:
            entry = self.requests.get(request_id)
            return (entry is not None and entry[0].active
                    and entry[0].installation_id == installation_id and not entry[1].done())

    def complete(self, request):
        with self.lock:
            entry = self.requests.get(request["id"])
        if entry is None:
            return
        owner, future = entry
        if future.done() or not owner.active:
            return
        error = request.get("error")
        try:
            if error:
                future.set_exception(RpcError(error.get("code", 0), error["name"], error.get("description", "")))
            else:
                future.set_result(request.get("result"))
        except InvalidStateError:
            pass

    def submit_ui(self, owner, method, **parameters):
        # Checked and sent under the lock that remove() holds while sending
        # "ui.close_plugin", so no command of an unloaded plugin follows it.
        with self.lock:
            if not owner.active:
                raise RuntimeError("Плагин уже выгружен.")
            self.submit({"id": uuid.uuid4().hex, "method": method,
                         "installation_id": owner.installation_id, **parameters})

    def add_surface(self, surface):
        with self.lock:
            if not surface.owner.active:
                raise RuntimeError("Плагин уже выгружен.")
            if surface.id in self.surfaces:
                raise RuntimeError("Окно уже показано.")
            self.surfaces[surface.id] = surface

    def ui_event(self, event):
        if event.get("type") == "element_click":
            self.element_click(event)
            return
        if event.get("type") in ("widget_click", "key", "compose_changed", "menu_click",
                                  "native_window", "native_signal"):
            self.widget_rule_event(event)
            return
        with self.lock:
            surface = self.surfaces.get(event.get("object_id"))
        if surface is None or surface.owner.installation_id != event.get("installation_id"):
            installation_id = event.get("installation_id")
            if event.get("type") == "error" and installation_id in self.contexts:
                self.manager.report_error(installation_id, str(event.get("value", "")))
            return
        owner = surface.owner
        kind = event.get("type")
        if kind == "error":
            if event.get("closed"):
                with self.lock:
                    self.surfaces.pop(surface.id, None)
                surface.closed = True
            self.manager.report_error(owner.installation_id, str(event.get("value", "")))
            return
        if kind == "closed":
            with self.lock:
                self.surfaces.pop(surface.id, None)
            surface.closed = True
            callback = surface.on_close
        else:
            node = surface.nodes.get(event.get("node_id"))
            callback = node.handlers.get(kind) if node is not None else None
            if kind in ("change", "toggle") and node is not None:
                node.props["text" if kind == "change" else "value"] = event.get("value")
        if callback is None or not owner.active:
            return
        try:
            value = event.get("value")
            result = (self.call(owner, callback) if value is None
                      else self.call(owner, callback, *value) if isinstance(value, list)
                      else self.call(owner, callback, value))
            if inspect.iscoroutine(result):
                self.schedule(owner, result)
        except BaseException as error:
            self.manager.report_error(owner.installation_id, str(error) or type(error).__name__)

    def element_click(self, event):
        installation_id = event.get("installation_id")
        with self.lock:
            callback = self.element_handlers.get((installation_id, event.get("element")))
        owner = self.contexts.get(installation_id)
        if callback is None or owner is None or not owner.active:
            return
        try:
            result = self.call(owner, callback)
            if inspect.iscoroutine(result):
                self.schedule(owner, result)
        except BaseException as error:
            self.manager.report_error(installation_id, str(error) or type(error).__name__)

    def widget_rule_event(self, event):
        with self.lock:
            entry = self.widget_rules.get(event.get("rule_id"))
        if entry is None:
            return
        owner, callback = entry
        if not owner.active or owner.installation_id != event.get("installation_id"):
            return
        try:
            value = event.get("value")
            result = self.call(owner, callback) if value is None else self.call(owner, callback, value)
            if inspect.iscoroutine(result):
                self.schedule(owner, result)
        except BaseException as error:
            self.manager.report_error(owner.installation_id, str(error) or type(error).__name__)

    def execute_ui(self, call_id):
        with self.lock:
            entry = self.ui_calls.pop(call_id, None)
        if entry is None:
            return
        owner, callback, future = entry
        if not owner.active or future.done():
            future.cancel()
            return
        try:
            result = self.call(owner, callback)
            if inspect.isawaitable(result):
                if inspect.iscoroutine(result):
                    result.close()
                raise TypeError("run_on_ui принимает синхронную функцию.")
            future.set_result(result)
        except BaseException as error:
            future.set_exception(error)

    def native_event(self, event):
        from .models import Event, chat_from_native, message_from_native
        if event["point"] in ("raw_update", "raw_updates", "raw_message"):
            self.update_event(event)
            return
        message = event.get("message")
        chat = event.get("chat")
        value = Event(str(event["account_id"]),
                      message_from_native(message) if message is not None else None,
                      chat_from_native(chat) if chat is not None else None,
                      tuple(event.get("message_ids", ())),
                      int(message["chat_id"]) if message is not None else None)
        self.emit(event["point"], value)

    def update_event(self, event):
        from .models import Event, Message, message_from_tl
        if not self.hook_mask & (POINT_BITS["new_message"] | POINT_BITS["edited_message"] | POINT_BITS["deleted_message"]):
            return
        data = base64.b64decode(event["data"], validate=True)
        account = str(event["account_id"])
        key = (account, hashlib.sha256(data).digest())
        if key in self.seen_events:
            return
        self.seen_events[key] = None
        if len(self.seen_events) > 2048:
            self.seen_events.popitem(last=False)
        kind = {"raw_updates": "Updates", "raw_update": "Update", "raw_message": "Message"}[event["point"]]
        value = tl.decode(data, kind)
        name = value.constructor_name
        if kind == "Message":
            if name in ("message", "messageService"):
                message = message_from_tl(account, value)
                self.emit("new_message", Event(account, message=message, chat_id=message.chat_id))
        elif name in ("updateNewMessage", "updateNewChannelMessage", "updateEditMessage", "updateEditChannelMessage"):
            if value.message.constructor_name not in ("message", "messageService"):
                return
            message = message_from_tl(account, value.message)
            self.emit("edited_message" if name.startswith("updateEdit") else "new_message",
                      Event(account, message=message, chat_id=message.chat_id))
        elif name in ("updateDeleteMessages", "updateDeleteChannelMessages"):
            chat_id = (value.channel_id | (2 << 48)) if name == "updateDeleteChannelMessages" else None
            self.emit("deleted_message", Event(account, message_ids=tuple(value.messages), chat_id=chat_id))
        elif name in ("updateShortMessage", "updateShortChatMessage"):
            chat_id = value.user_id if name == "updateShortMessage" else value.chat_id | (1 << 48)
            message = Message(account, value.id, chat_id, value.message, value.date, value.out)
            self.emit("new_message", Event(account, message=message, chat_id=chat_id))

    def emit(self, point, event):
        if point == "new_message" and event.message is not None:
            key = (event.account_id, event.message.chat_id, event.message.id)
            if key in self.seen_messages:
                return
            self.seen_messages[key] = None
            if len(self.seen_messages) > 2048:
                self.seen_messages.popitem(last=False)
        for handler in self.handlers(point):
            owner = self.contexts.get(handler.installation_id)
            if not handler.active or owner is None or not owner.active:
                continue
            try:
                result = self.call(owner, handler.callback, copy.deepcopy(event))
                if inspect.iscoroutine(result):
                    self.schedule(owner, result)
            except BaseException as error:
                self.manager.report_error(handler.installation_id, str(error))

    def remove(self, installation_id):
        for entry in self.registrations:
            if entry.installation_id == installation_id:
                entry.cancel()
        self.registrations = [entry for entry in self.registrations if entry.active]
        self.refresh_mask()
        with self.lock:
            for task in self.tasks.pop(installation_id, set()):
                task.cancel()
            pending = [key for key, (owner, _) in self.requests.items() if owner.installation_id == installation_id]
            for key in pending:
                _, future = self.requests.pop(key)
                future.cancel()
            for key, item in list(self.ui_calls.items()):
                if item[0].installation_id == installation_id:
                    self.ui_calls.pop(key)
                    item[2].cancel()
            for key in [key for key in self.element_handlers if key[0] == installation_id]:
                self.element_handlers.pop(key)
            for key in [key for key, (owner, _) in self.widget_rules.items()
                        if owner.installation_id == installation_id]:
                self.widget_rules.pop(key)
            surfaces = [key for key, item in self.surfaces.items() if item.owner.installation_id == installation_id]
            for key in surfaces:
                self.surfaces.pop(key).closed = True
            if installation_id in self.contexts:
                self.contexts[installation_id].active = False
            try:
                # Also closes UI the plugin queued before its surfaces were registered.
                self.submit({"method": "ui.close_plugin", "id": uuid.uuid4().hex, "installation_id": installation_id})
            except RuntimeError:
                pass
        for key in pending:
            try:
                self.submit({"method": "cancel", "id": key, "installation_id": installation_id})
            except RuntimeError:
                pass
        self.contexts.pop(installation_id, None)

    def stop(self):
        self.stopping = True
        if self.loop is None:
            return

        async def finish():
            current = asyncio.current_task()
            pending = [task for task in asyncio.all_tasks() if task is not current]
            for task in pending:
                task.cancel()
            await asyncio.gather(*pending, return_exceptions=True)

        future = asyncio.run_coroutine_threadsafe(finish(), self.loop)
        try:
            future.result(timeout=2)
        except TimeoutError:
            self.manager.restart_required = True
            return
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join(timeout=2)

    @staticmethod
    def log_hook_skip(point, error):
        print(f"Ovygram: {point} skipped, can't decode TL: {error}", file=sys.stderr)

    def native_hook(self, request):
        point = request["point"]
        account = request["account_id"]
        inherited = tuple(request.get("hook_stack", ()))
        data = base64.b64decode(request["data"], validate=True)
        if not self.handlers(point) and (point != "before_rpc" or not self.handlers("before_send")):
            return {"data": request["data"], "error": request.get("error")}
        if point == "before_rpc":
            name = self.function_name(data)
            if name is None or not (self.wanted("before_rpc", name) or (
                    name in OUTGOING and self.wanted("before_send", name))):
                return {"data": request["data"]}
            value = RpcContext(account, request["request_id"], tl.decode(data))

            def validate(value, original):
                if (not isinstance(value, RpcContext) or value.account_id != original.account_id
                        or value.request_id != original.request_id
                        or value.request.constructor_name != original.request.constructor_name):
                    raise HookError("Хук изменил аккаунт, ID или тип запроса.")
                if original.request.constructor_name.startswith("messages.send") or original.request.constructor_name == "messages.forwardMessages":
                    for field in ("peer", "from_peer", "to_peer", "random_id"):
                        if (hasattr(original.request, field)
                                and getattr(value.request, field) != getattr(original.request, field)):
                            raise HookError("Хук отправки не может менять получателя или random_id.")
                    if hasattr(original.request, "multi_media"):
                        if [item.random_id for item in value.request.multi_media] != [item.random_id for item in original.request.multi_media]:
                            raise HookError("Хук альбома должен сохранить состав random_id.")
                tl.encode(value.request)

            if value.request.constructor_name in OUTGOING:
                message = OutgoingMessage(account, copy.deepcopy(value.request))

                def validate_message(changed, original):
                    if not isinstance(changed, OutgoingMessage) or changed.account_id != account:
                        raise HookError("Некорректный результат before_send.")
                    validate(RpcContext(account, value.request_id, changed.request), value)

                message = self.hooks("before_send", message, validate_message, inherited)
                value.request = message.request
            value = self.hooks(point, value, validate, inherited)
            changed = tl.encode(value.request)
            local_texts = []
            if changed != data and value.request.constructor_name in ("messages.sendMessage", "messages.sendMedia", "messages.sendMultiMedia"):
                items = value.request.multi_media if hasattr(value.request, "multi_media") else [value.request]
                for item in items:
                    text = tl.textWithEntities(text=item.message, entities=item.entities or [])
                    local_texts.append({"random_id": str(item.random_id),
                                        "text": base64.b64encode(tl.encode(text)).decode("ascii")})
            return {"data": base64.b64encode(changed).decode("ascii"), "local_texts": local_texts}
        if point == "before_updates":
            try:
                updates = tl.decode(data, "Updates")
            except Exception as error:
                # Never drop server updates because the SDK can't read them.
                self.log_hook_skip(point, error)
                return {"data": request["data"]}
            value = UpdateContext(account, updates)

            def validate(changed, original):
                if (not isinstance(changed, UpdateContext) or changed.account_id != account
                        or not isinstance(changed.updates, tl.TLObject)
                        or changed.updates._tl["result"] != "Updates"):
                    raise HookError("Хук обновлений должен вернуть Updates.")
                tl.encode(changed.updates)

            value = self.hooks(point, value, validate, inherited)
            return {"data": base64.b64encode(tl.encode(value.updates)).decode("ascii")}
        if point == "after_rpc":
            request_data = base64.b64decode(request.get("request_data") or "")
            name = self.function_name(request_data)
            if not self.wanted(point, name):
                return {"data": request["data"], "error": request.get("error")}
            try:
                original_request = tl.decode(request_data) if name else None
            except Exception as error:
                self.log_hook_skip(point, error)
                original_request = None
            value = RpcResponse(account, request["request_id"], data or None,
                                request.get("error"), original_request)

            def validate(changed, original):
                if (not isinstance(changed, RpcResponse) or changed.account_id != account
                        or changed.request_id != original.request_id
                        or changed.request != original.request
                        or (changed.response is None) == (changed.error is None)):
                    raise HookError("Некорректный ответ RPC.")
                if changed.response is not None:
                    if not isinstance(changed.response, bytes) or len(changed.response) % 4:
                        raise HookError("Некорректные TL-байты ответа.")
                    if changed.request is not None:
                        tl.decode(changed.response, tl.response_type(changed.request))
                elif (not isinstance(changed.error, dict)
                      or type(changed.error.get("code")) is not int
                      or not isinstance(changed.error.get("name"), str)
                      or not isinstance(changed.error.get("description", ""), str)):
                    raise HookError("Некорректная RPC-ошибка.")

            value = self.hooks(point, value, validate, inherited)
            return {"data": base64.b64encode(value.response or b"").decode("ascii"), "error": value.error}
        raise HookError("Неизвестная точка перехвата.")
