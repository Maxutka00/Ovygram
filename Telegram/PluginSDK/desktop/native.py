"""Low-level access to Telegram's Qt objects.

Window events, Qt signals and invokable methods of any widget from
desktop.ui.widget_tree(). Telegram's internals change between versions, so
prefer desktop.ui where it is enough; class and method names here are
Telegram's own. Calling methods can break the client like any plugin code.
Everything is undone when the plugin is unloaded.
"""

from ._runtime import context
from .ui import WidgetRule, _handle


def on_window(callback):
    """Calls callback(event) when a top-level window, dialog or popup menu
    is shown or hidden. event is a dict with event ("shown" or "hidden"),
    handle, cls, kind ("window", "dialog", "popup", "other") and title.
    Returns a rule with remove()."""
    if not callable(callback):
        raise TypeError("callback должен быть функцией.")
    return WidgetRule(context(), "ui.native.windows", callback, enabled=True)


def connect(widget, signal, callback):
    """Calls callback(*arguments) on each emission of a Qt signal of the
    widget, e.g. "windowTitleChanged" or "windowTitleChanged(QString)".
    Arguments are converted to JSON values where possible. The connection
    ends with remove(), when the widget is destroyed or on unload."""
    if not isinstance(signal, str) or not signal:
        raise ValueError("Укажи имя сигнала.")
    if not callable(callback):
        raise TypeError("callback должен быть функцией.")
    return WidgetRule(context(), "ui.native.connect", lambda arguments: callback(*arguments),
                      handle=_handle(widget), signal=signal)


async def methods(widget):
    """Public signals, slots and invokable methods of the widget: a list of
    dicts with name, signature, type ("signal", "slot", "method") and returns."""
    owner = context()
    return await owner.manager.runtime.request("native.methods", handle=_handle(widget))


async def invoke(widget, name, *arguments):
    """Calls a public slot or invokable method by name on the main thread
    and returns its result. Arguments are converted to the parameter types;
    an overload with as many parameters that accepts them is chosen."""
    if not isinstance(name, str) or not name:
        raise ValueError("Укажи имя метода.")
    owner = context()
    return await owner.manager.runtime.request(
        "native.invoke", handle=_handle(widget), name=name, args=list(arguments))
