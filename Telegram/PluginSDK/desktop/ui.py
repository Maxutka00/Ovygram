"""Plugin dialogs, windows and widgets described by a tree of nodes.

Every call only queues a command for the client, so it can be made from
on_plugin_load, a hook or a background task. The client builds the widgets
on the main thread, and widget callbacks always run on the main thread.
"""

import uuid
from dataclasses import dataclass

from ._runtime import context


class ObjectDestroyed(RuntimeError):
    """The dialog or window was closed, or its plugin was unloaded."""


def _identity():
    return uuid.uuid4().hex


def _layout(width=None, stretch=None):
    """Size of a node inside a Row: a fixed width in pixels, "fit" for its
    natural width, or a share of the remaining width (stretch, default 1)."""
    result = {}
    if width is not None:
        if width != "fit" and (type(width) is not int or width < 0):
            raise ValueError('width должен быть числом пикселей или "fit".')
        result["width"] = width
    if stretch is not None:
        if type(stretch) is not int or not 0 <= stretch <= 100:
            raise ValueError("stretch должен быть целым от 0 до 100.")
        result["stretch"] = stretch
    return result


def _choice(value, allowed, name):
    if value not in allowed:
        raise ValueError(f"{name} должен быть одним из: {', '.join(allowed)}.")
    return value


class Node:
    type = ""

    def __init__(self, width=None, stretch=None, **props):
        self.id = _identity()
        self.props = {**props, **_layout(width, stretch)}
        self.children = ()
        self.handlers = {}

    def to_json(self):
        result = {"type": self.type, "id": self.id, **self.props}
        if self.children:
            result["children"] = [child.to_json() for child in self.children]
        return result

    def walk(self):
        yield self
        for child in self.children:
            yield from child.walk()


class Column(Node):
    type = "column"

    def __init__(self, *children, width=None, stretch=None):
        super().__init__(width, stretch)
        self.children = tuple(_node(child) for child in children)


class Row(Node):
    """Children side by side. align is the vertical alignment of children:
    "top", "center" or "bottom"; spacing is the gap between them in pixels."""

    type = "row"

    def __init__(self, *children, align="center", spacing=8, width=None, stretch=None):
        if type(spacing) is not int or not 0 <= spacing <= 200:
            raise ValueError("spacing должен быть целым от 0 до 200.")
        super().__init__(width, stretch, align=_choice(align, ("top", "center", "bottom"), "align"),
                         spacing=spacing)
        self.children = tuple(_node(child) for child in children)


class Text(Node):
    """align is the horizontal alignment: "left", "center" or "right"."""

    type = "text"

    def __init__(self, text, align="left", width=None, stretch=None):
        super().__init__(width, stretch, text=str(text),
                         align=_choice(align, ("left", "center", "right"), "align"))


class Button(Node):
    type = "button"

    def __init__(self, text, on_click=None, width=None, stretch=None):
        super().__init__(width, stretch, text=str(text))
        if on_click is not None:
            self.handlers["click"] = on_click


class Input(Node):
    type = "input"

    def __init__(self, text="", placeholder="", on_change=None, width=None, stretch=None):
        super().__init__(width, stretch, text=str(text), placeholder=str(placeholder))
        if on_change is not None:
            self.handlers["change"] = on_change


class Switch(Node):
    type = "switch"

    def __init__(self, text, value=False, on_toggle=None, width=None, stretch=None):
        super().__init__(width, stretch, text=str(text), value=bool(value))
        if on_toggle is not None:
            self.handlers["toggle"] = on_toggle


class Image(Node):
    type = "image"

    def __init__(self, path, height=0, width=None, stretch=None):
        super().__init__(width, stretch, path=str(path), height=int(height))


class Spacer(Node):
    type = "spacer"

    def __init__(self, height, width=None, stretch=None):
        super().__init__(width, stretch, height=int(height))


class Canvas(Node):
    """Custom drawing: a list of draw commands, see the draw helpers below.

    Negative x or y count from the right or bottom edge, as in decorations."""

    type = "canvas"

    def __init__(self, height, commands=(), on_click=None, width=None, stretch=None):
        super().__init__(width, stretch, height=int(height), commands=list(commands))
        if on_click is not None:
            self.handlers["click"] = on_click


def fill_rect(x, y, width, height, color, radius=0):
    return {"op": "rect", "x": x, "y": y, "width": width, "height": height,
            "color": color, "radius": radius}


def line(x1, y1, x2, y2, color, width=1):
    return {"op": "line", "x1": x1, "y1": y1, "x2": x2, "y2": y2, "color": color, "width": width}


def ellipse(x, y, width, height, color):
    return {"op": "ellipse", "x": x, "y": y, "width": width, "height": height, "color": color}


def text(x, y, value, color, size=13):
    return {"op": "text", "x": x, "y": y, "text": str(value), "color": color, "size": size}


def _node(value):
    if isinstance(value, Node):
        return value
    if isinstance(value, str):
        return Text(value)
    raise TypeError("Элемент интерфейса должен быть Node или строкой.")


class Surface:
    """A shown dialog or window that belongs to the calling plugin."""

    kind = ""

    def __init__(self, content, title="", width=0, height=0, on_close=None):
        self.owner = context()
        self.id = _identity()
        self.content = _node(content)
        self.title = str(title)
        self.width = int(width)
        self.height = int(height)
        self.on_close = on_close
        self.closed = False
        self.nodes = {node.id: node for node in self.content.walk()}

    def show(self):
        runtime = self.owner.manager.runtime
        runtime.add_surface(self)
        runtime.submit_ui(self.owner, "ui.show", object_id=self.id, kind=self.kind,
                          title=self.title, width=self.width, height=self.height,
                          tree=self.content.to_json(), **self._placement())
        return self

    def _placement(self):
        return {}

    def update(self, node, **props):
        self._check(node)
        node.props.update(props)
        self.owner.manager.runtime.submit_ui(
            self.owner, "ui.update", object_id=self.id, node_id=node.id, props=props)

    def draw(self, canvas, commands):
        if not isinstance(canvas, Canvas):
            raise TypeError("draw принимает Canvas.")
        self.update(canvas, commands=list(commands))

    def close(self):
        if self.closed:
            return
        self.owner.manager.runtime.submit_ui(self.owner, "ui.close", object_id=self.id)

    def _check(self, node):
        if self.closed:
            raise ObjectDestroyed("Окно уже закрыто.")
        if self.nodes.get(getattr(node, "id", None)) is not node:
            raise ValueError("Элемент не принадлежит этому окну.")


class Dialog(Surface):
    """A modal box in the active Telegram window."""

    kind = "dialog"


class Window(Surface):
    """A separate floating window."""

    kind = "window"

    def __init__(self, content, title="", width=420, height=480, on_close=None):
        super().__init__(content, title, width, height, on_close)


class ChatBar(Surface):
    """A bar above the messages of one chat, below Telegram's own bars.

    The bar is shown while that chat is open in a window and stays until
    close() or until the plugin is unloaded.
    """

    kind = "chat_bar"

    def __init__(self, chat, content, on_close=None):
        account_id = getattr(chat, "account_id", None)
        chat_id = getattr(chat, "id", None)
        if not account_id or chat_id is None:
            raise TypeError("ChatBar принимает Chat из desktop.client.")
        super().__init__(content, on_close=on_close)
        self.account_id = str(account_id)
        self.chat_id = str(chat_id)

    def _placement(self):
        return {"account_id": self.account_id, "chat_id": self.chat_id}


class Section(Surface):
    """A page in the main column of the active window, in place of a chat.

    It has a back button and the title on top, and the content scrolls.
    Back and the window history work as for Telegram's own pages: the user
    can open a chat and come back. The section is closed by close(), when
    the window history drops it (on_close is called then) or on unload.
    """

    kind = "section"

    def __init__(self, content, title="", on_close=None):
        super().__init__(content, title, on_close=on_close)


# Built-in Telegram widgets a plugin can change. The names stay the same
# across Telegram updates; each one may exist once per open window.
ELEMENTS = (
    "chat.top_bar.call",
    "chat.top_bar.search",
    "chat.top_bar.info",
    "chat.top_bar.menu",
    # Hiding compose.attach leaves a gap: Telegram reserves its width.
    "compose.attach",
    "compose.emoji",
    "compose.send",
    "compose.field",
)


class Element:
    """A built-in Telegram widget. Changes belong to the calling plugin and
    are undone when it is unloaded."""

    def __init__(self, name):
        if name not in ELEMENTS:
            raise ValueError(f"Неизвестный элемент {name!r}. Доступны: {', '.join(ELEMENTS)}.")
        self.owner = context()
        self.name = name

    def hide(self):
        self.owner.manager.runtime.submit_ui(self.owner, "ui.element.hide", element=self.name, hidden=True)

    def show(self):
        """Removes this plugin's hide rule; Telegram decides the visibility again."""
        self.owner.manager.runtime.submit_ui(self.owner, "ui.element.hide", element=self.name, hidden=False)

    def on_click(self, callback, replace=False):
        """Calls callback() on click. With replace=True Telegram's own action
        is not run."""
        if not callable(callback):
            raise TypeError("callback должен быть функцией.")
        runtime = self.owner.manager.runtime
        with runtime.lock:
            runtime.element_handlers[(self.owner.plugin_id, self.name)] = callback
        runtime.submit_ui(self.owner, "ui.element.click", element=self.name,
                          enabled=True, replace=bool(replace))

    def off_click(self):
        runtime = self.owner.manager.runtime
        with runtime.lock:
            runtime.element_handlers.pop((self.owner.plugin_id, self.name), None)
        runtime.submit_ui(self.owner, "ui.element.click", element=self.name, enabled=False)


def element(name):
    return Element(name)


def set_colors(colors):
    """Changes palette colors, e.g. {"windowBg": "#101820"}. Names are the
    keys of a Telegram .tdesktop-theme. Undone by reset_colors() or unload."""
    if not isinstance(colors, dict) or not colors:
        raise ValueError("Ожидается непустой словарь цветов.")
    for key, value in colors.items():
        if not isinstance(key, str) or not isinstance(value, str) or not value.startswith("#"):
            raise ValueError("Цвет задаётся строкой #rrggbb или #aarrggbb.")
    owner = context()
    owner.manager.runtime.submit_ui(owner, "ui.palette", colors=dict(colors))


def reset_colors():
    owner = context()
    owner.manager.runtime.submit_ui(owner, "ui.palette", reset=True)


class Overlay(Surface):
    """A Canvas drawn over any widget from widget_tree(); it follows the
    widget's size. Without on_click on the canvas, clicks pass through."""

    kind = "overlay"

    def __init__(self, target, canvas, on_close=None):
        if not isinstance(canvas, Canvas):
            raise TypeError("Overlay принимает Canvas.")
        super().__init__(canvas, on_close=on_close)
        self.target = _handle(target)

    def _placement(self):
        return {"target": self.target, "clickable": "click" in self.content.handlers}


# Generic access to any Telegram widget. Widgets are found by a selector,
# so a rule also applies to widgets created later, e.g. in a new chat:
#   cls       class name from widget_tree(), e.g. "Ui::IconButton"
#   ancestor  class name of any parent, e.g. "HistoryView::TopBarWidget"
#   name      Qt objectName
#   accessible accessible name (localized, as shown by widget_tree())
#   element   a name from ELEMENTS
#   index     position among matching siblings, from 0
_SELECTOR_KEYS = ("cls", "ancestor", "name", "accessible", "element", "index")


def _selector(selector):
    unknown = set(selector) - set(_SELECTOR_KEYS)
    if unknown:
        raise ValueError(f"Неизвестные поля селектора: {', '.join(sorted(unknown))}.")
    if not any(selector.get(key) for key in ("cls", "name", "accessible", "element")):
        raise ValueError("Селектору нужен cls, name, accessible или element.")
    if "index" in selector and (type(selector["index"]) is not int or selector["index"] < 0):
        raise ValueError("index должен быть неотрицательным целым.")
    return {key: value for key, value in selector.items() if value is not None}


def _handle(value):
    handle = value.get("handle") if isinstance(value, dict) else value
    if not isinstance(handle, str) or not handle.isdigit():
        raise ValueError("Ожидается узел или handle из widget_tree().")
    return handle


class WidgetRule:
    """A rule owned by the calling plugin; undone by remove() or unload."""

    def __init__(self, owner, method, callback=None, **parameters):
        self.owner = owner
        self.id = _identity()
        self.method = method
        self.removed = False
        runtime = owner.manager.runtime
        if callback is not None:
            with runtime.lock:
                runtime.widget_rules[self.id] = (owner, callback)
        runtime.submit_ui(owner, method, rule_id=self.id, **parameters)

    def remove(self):
        runtime = self.owner.manager.runtime
        with runtime.lock:
            if runtime.widget_rules.pop(self.id, None) is None and self.removed:
                return
        self.removed = True
        if not self.owner.active:
            return
        if self.method == "ui.compose.watch":
            runtime.submit_ui(self.owner, "ui.compose.watch", rule_id=self.id, enabled=False)
        elif self.method == "ui.menu.add":
            runtime.submit_ui(self.owner, "ui.menu.remove", rule_id=self.id)
        elif self.method.startswith("ui.native."):
            runtime.submit_ui(self.owner, "ui.native.disconnect", rule_id=self.id)
        else:
            runtime.submit_ui(self.owner, "ui.widgets.unrule", rule_id=self.id)


async def widget_tree(depth=8, root=None):
    """The widget tree of the active window as nested dicts with handle,
    cls, visible, geometry, and name, accessible, element and children
    when present. Handles stay valid while the widget exists."""
    owner = context()
    return await owner.manager.runtime.request(
        "widgets.tree", depth=int(depth), root=_handle(root) if root is not None else None)


async def get_property(widget, name):
    """Reads a Qt property, e.g. "geometry", "visible", "toolTip"."""
    owner = context()
    return await owner.manager.runtime.request("widgets.get", handle=_handle(widget), property=str(name))


def set_property(widget, name, value):
    """Writes a Qt property. Telegram may overwrite it on its next layout."""
    owner = context()
    owner.manager.runtime.submit_ui(owner, "ui.widgets.set", handle=_handle(widget),
                                    property=str(name), value=value)


def hide_widgets(**selector):
    """Hides matching widgets now and whenever Telegram shows them again.
    The parent is not relaid out, so a gap may remain; use element() for
    the named elements, which close the gap."""
    return WidgetRule(context(), "ui.widgets.rule", action="hide", selector=_selector(selector))


def on_widget_click(callback, replace=False, **selector):
    if not callable(callback):
        raise TypeError("callback должен быть функцией.")
    return WidgetRule(context(), "ui.widgets.rule", callback, action="click",
                      replace=bool(replace), selector=_selector(selector))


def on_key(sequence, callback, replace=False, element=None):
    """Calls callback() on a key combination like "Ctrl+Alt+K". With
    replace=True Telegram doesn't receive the key, and the rule also wins
    over Telegram's own shortcuts. With element, e.g. "compose.field", the
    rule works only while the focus is inside that element. Keys taken by
    the system or the input method (e.g. Ctrl+Shift+U in IBus) never reach
    Telegram."""
    if not isinstance(sequence, str) or not sequence:
        raise ValueError("Ожидается сочетание клавиш, например Ctrl+Alt+K.")
    if not callable(callback):
        raise TypeError("callback должен быть функцией.")
    if element is not None and element not in ELEMENTS:
        raise ValueError(f"Неизвестный элемент {element!r}.")
    return WidgetRule(context(), "ui.keys.add", callback, sequence=sequence,
                      replace=bool(replace), element=element or "")


class ChatDecoration:
    """Draw commands painted over a chat's row in the chat list.

    Coordinates are relative to the row; negative x or y count from its
    right or bottom edge, e.g. fill_rect(-28, 8, 20, 20, ...) is a square
    near the right edge. background tints the whole row, except when the
    chat is open. Everything is painted over the row, so use a translucent
    #aarrggbb background: an opaque one hides the row's text. Undone by
    remove() or when the plugin is unloaded."""

    def __init__(self, owner, account_id, chat_id, commands, background):
        self.owner = owner
        self.id = _identity()
        self.account_id = account_id
        self.chat_id = chat_id
        self.update(commands, background)

    def update(self, commands=(), background=None):
        if background is not None and (not isinstance(background, str) or not background.startswith("#")):
            raise ValueError("background задаётся строкой #rrggbb или #aarrggbb.")
        self.owner.manager.runtime.submit_ui(
            self.owner, "ui.decoration.set", decoration_id=self.id, account_id=self.account_id,
            chat_id=self.chat_id, commands=list(commands), background=background)

    def remove(self):
        if self.owner.active:
            self.owner.manager.runtime.submit_ui(self.owner, "ui.decoration.remove", decoration_id=self.id)


def decorate_chat(chat, commands=(), background=None, account=None):
    """Decorates one chat's row, or every chat of an account when chat is
    "*" and account is given (an Account or account ID)."""
    if chat == "*":
        account_id = getattr(account, "id", account)
        if not isinstance(account_id, str) or not account_id:
            raise ValueError('Для chat="*" укажи account.')
        return ChatDecoration(context(), account_id, "*", commands, background)
    account_id = getattr(chat, "account_id", None)
    chat_id = getattr(chat, "id", None)
    if not account_id or chat_id is None:
        raise TypeError('decorate_chat принимает Chat из desktop.client или "*".')
    return ChatDecoration(context(), str(account_id), str(chat_id), commands, background)


def on_compose_change(callback):
    """Calls callback(state) when the user edits the message field. state
    is a dict with text, cursor, selection_start and selection_end; the
    positions index state["text"]. Returns a rule with remove()."""
    if not callable(callback):
        raise TypeError("callback должен быть функцией.")
    return WidgetRule(context(), "ui.compose.watch", callback, enabled=True)


async def compose_state():
    """The same state dict for the message field in the active window, or None."""
    owner = context()
    return await owner.manager.runtime.request("compose.get_state")


def replace_compose_text(start, end, text, select=False):
    """Replaces text between positions start and end of the message field,
    keeping the formatting of the rest. With select=True the inserted text
    stays selected, like an inline suggestion."""
    if type(start) is not int or type(end) is not int or not 0 <= start <= end:
        raise ValueError("Ожидаются позиции 0 <= start <= end.")
    owner = context()
    owner.manager.runtime.submit_ui(owner, "ui.compose.replace", start=start, end=end,
                                    text=str(text), select=bool(select))


class MessageDecoration:
    """Draw commands painted over a message bubble, in bubble coordinates;
    negative x or y count from the bubble's right or bottom edge.
    background tints the bubble. Undone by remove() or unload."""

    def __init__(self, owner, message, commands, background):
        self.owner = owner
        self.id = _identity()
        self.account_id = str(message.account_id)
        self.chat_id = str(message.chat_id)
        self.message_id = int(message.id)
        self.update(commands, background)

    def update(self, commands=(), background=None):
        if background is not None and (not isinstance(background, str) or not background.startswith("#")):
            raise ValueError("background задаётся строкой #rrggbb или #aarrggbb.")
        self.owner.manager.runtime.submit_ui(
            self.owner, "ui.message_decoration.set", decoration_id=self.id,
            account_id=self.account_id, chat_id=self.chat_id, message_id=self.message_id,
            commands=list(commands), background=background)

    def remove(self):
        if self.owner.active:
            self.owner.manager.runtime.submit_ui(
                self.owner, "ui.message_decoration.remove", decoration_id=self.id)


def decorate_message(message, commands=(), background=None):
    """Decorates a Message from desktop.client or an event.

    Painted over the bubble, so use a translucent #aarrggbb background: an
    opaque one hides the message text."""
    if not all(hasattr(message, key) for key in ("account_id", "chat_id", "id")):
        raise TypeError("decorate_message принимает Message из desktop.client.")
    return MessageDecoration(context(), message, commands, background)


class HiddenChats:
    """Chats hidden from the chat list and its folders by the calling
    plugin. Search still finds them. Undone by remove() or unload."""

    def __init__(self, owner, chats):
        self.owner = owner
        self.id = _identity()
        self.accounts = {}
        for chat in chats:
            account_id = getattr(chat, "account_id", None)
            chat_id = getattr(chat, "id", None)
            if not account_id or chat_id is None:
                raise TypeError("hide_chats принимает Chat из desktop.client.")
            self.accounts.setdefault(str(account_id), set()).add(str(chat_id))
        if not self.accounts:
            raise ValueError("Укажи хотя бы один чат.")
        for account_id, chat_ids in self.accounts.items():
            owner.manager.runtime.submit_ui(
                owner, "ui.chat_list.hide", rule_id=f"{self.id}:{account_id}",
                account_id=account_id, chat_ids=sorted(chat_ids))

    def remove(self):
        if not self.owner.active:
            return
        for account_id in self.accounts:
            self.owner.manager.runtime.submit_ui(
                self.owner, "ui.chat_list.unhide", rule_id=f"{self.id}:{account_id}")
        self.accounts = {}


def hide_chats(chats):
    """Hides chats (Chat objects, possibly from several accounts)."""
    return HiddenChats(context(), list(chats))


async def compose_text():
    """Text of the message field in the active window, or None."""
    owner = context()
    return await owner.manager.runtime.request("compose.get_text")


def set_compose_text(text):
    """Replaces the text of the message field in the active window."""
    owner = context()
    owner.manager.runtime.submit_ui(owner, "ui.compose.set", text=str(text))


def insert_compose_text(text):
    """Inserts text at the cursor of the message field in the active window."""
    owner = context()
    owner.manager.runtime.submit_ui(owner, "ui.compose.insert", text=str(text))


def set_clipboard(text):
    """Puts text into the system clipboard."""
    owner = context()
    owner.manager.runtime.submit_ui(owner, "ui.clipboard", text=str(text))


def show_dialog(content, title="", width=0, on_close=None):
    return Dialog(content, title, width, on_close=on_close).show()


@dataclass(frozen=True)
class MenuContext:
    """Where a plugin menu item was clicked.

    account_id is the account of the window. chat is the chat of a "chat" or
    "message" menu, message the message of a "message" menu, otherwise None."""

    account_id: str
    chat: object = None
    message: object = None


_MENUS = ("main", "chat", "message")
_CHAT_KINDS = ("user", "chat", "channel")


def add_menu_item(menu, text, callback, kinds=None):
    """Adds an item to a Telegram menu, after its own items.

    menu is "main" (the side menu), "chat" (the chat's "⋮" menu and its
    context menu in the chat list) or "message" (a message's context menu).
    callback(context) gets a MenuContext; it may be a coroutine function.
    kinds limits a "chat" or "message" item to chats of these kinds: "user",
    "chat" (basic group), "channel" (also supergroups). The item shows from
    the next time the menu opens. Returns a rule with remove()."""
    _choice(menu, _MENUS, "menu")
    if not isinstance(text, str) or not 1 <= len(text.strip()) <= 64:
        raise ValueError("Текст пункта меню: от 1 до 64 символов.")
    if not callable(callback):
        raise TypeError("callback должен быть функцией.")
    if kinds is not None:
        if menu == "main":
            raise ValueError("kinds применим только к меню chat и message.")
        kinds = list(kinds)
        if not kinds or any(kind not in _CHAT_KINDS for kind in kinds):
            raise ValueError("kinds: непустой список из user, chat, channel.")

    def clicked(value):
        from .models import chat_from_native, message_from_native
        chat = value.get("chat")
        message = value.get("message")
        return callback(MenuContext(
            str(value.get("account_id", "")),
            chat_from_native(chat) if chat else None,
            message_from_native(message) if message else None))

    return WidgetRule(context(), "ui.menu.add", clicked, menu=menu, text=text.strip(),
                      kinds=kinds or [])
