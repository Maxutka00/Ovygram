import json
from pathlib import Path
import queue
import sys
import tempfile
import threading
import unittest


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "Telegram/PluginSDK"))

import base64

from desktop import tl, ui
from desktop._runtime import _current
from desktop.models import Event, Message
from ovygram_runtime import Manager


class DesktopUiTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.manager = Manager(self.root / "profile")
        self.addCleanup(self.manager.shutdown)
        self.runtime = self.manager.runtime
        self.commands = queue.Queue()
        self.runtime.sender = self.commands.put
        self.runtime.ready.set()
        self.owners = {}
        for identity in ("plugin.a", "plugin.b"):
            source = self.root / (identity + ".plugin")
            source.write_text(
                'from base_plugin import BasePlugin\n'
                f'__id__ = {identity!r}\n__name__ = "Test"\n__version__ = "1.0"\n'
                '__author__ = "Test"\n__description__ = "Test"\n'
                '__platform__ = "desktop"\n__desktop_sdk__ = 1\n'
                'class TestPlugin(BasePlugin):\n    pass\n', encoding="utf-8")
            self.manager.install(str(source))
            self.manager.enable(identity)
            self.owners[identity] = self.manager.loaded[identity][1]

    def as_plugin(self, identity, function):
        token = _current.set(self.owners[identity])
        try:
            return function()
        finally:
            _current.reset(token)

    def event(self, **event):
        response = json.loads(self.manager.dispatch(json.dumps({"action": "ui_event", "event": event})))
        self.assertIn("result", response, response)

    def commands_list(self):
        result = []
        while not self.commands.empty():
            result.append(self.commands.get_nowait())
        return result

    def test_dialog_tree_is_sent_and_callbacks_run(self):
        clicks, changes = [], []
        button = ui.Button("Нажми", on_click=lambda: clicks.append(True))
        field = ui.Input("а", on_change=changes.append)
        dialog = self.as_plugin("plugin.a", lambda: ui.show_dialog(
            ui.Column("Заголовок", ui.Row(button, field)), title="Тест"))
        command = self.commands_list()[-1]
        self.assertEqual(command["method"], "ui.show")
        self.assertEqual(command["plugin_id"], "plugin.a")
        self.assertEqual(command["kind"], "dialog")
        tree = command["tree"]
        self.assertEqual([child["type"] for child in tree["children"]], ["text", "row"])
        self.assertEqual(tree["children"][1]["children"][0]["id"], button.id)
        self.event(plugin_id="plugin.a", object_id=dialog.id, node_id=button.id, type="click")
        self.event(plugin_id="plugin.a", object_id=dialog.id, node_id=field.id, type="change", value="аб")
        self.assertEqual(clicks, [True])
        self.assertEqual(changes, ["аб"])
        self.assertEqual(field.props["text"], "аб")

    def test_events_from_another_plugin_are_ignored(self):
        clicks = []
        button = ui.Button("x", on_click=lambda: clicks.append(True))
        dialog = self.as_plugin("plugin.a", lambda: ui.show_dialog(button))
        self.event(plugin_id="plugin.b", object_id=dialog.id, node_id=button.id, type="click")
        self.assertEqual(clicks, [])

    def test_closed_surface_raises_object_destroyed(self):
        closed = []
        label = ui.Text("x")
        dialog = self.as_plugin("plugin.a", lambda: ui.show_dialog(label, on_close=lambda: closed.append(1)))
        self.event(plugin_id="plugin.a", object_id=dialog.id, node_id="", type="closed")
        self.assertTrue(dialog.closed)
        self.assertEqual(closed, [1])
        with self.assertRaises(ui.ObjectDestroyed):
            self.as_plugin("plugin.a", lambda: dialog.update(label, text="y"))

    def test_show_error_closes_the_surface_and_reports(self):
        dialog = self.as_plugin("plugin.a", lambda: ui.show_dialog("x"))
        self.event(plugin_id="plugin.a", object_id=dialog.id, type="error", value="bad tree", closed=True)
        self.assertTrue(dialog.closed)
        self.assertEqual(self.manager.errors["plugin.a"], "bad tree")

    def test_callback_error_is_reported_without_breaking_dispatch(self):
        button = ui.Button("x", on_click=lambda: 1 / 0)
        dialog = self.as_plugin("plugin.a", lambda: ui.show_dialog(button))
        self.event(plugin_id="plugin.a", object_id=dialog.id, node_id=button.id, type="click")
        self.assertIn("division", self.manager.errors["plugin.a"])

    def test_canvas_click_and_draw(self):
        points = []
        canvas = ui.Canvas(100, [ui.fill_rect(0, 0, 10, 10, "#ff0000")], on_click=lambda x, y: points.append((x, y)))
        window = self.as_plugin("plugin.a", lambda: ui.Window(canvas, "Холст").show())
        self.assertEqual(self.commands_list()[-1]["kind"], "window")
        self.event(plugin_id="plugin.a", object_id=window.id, node_id=canvas.id, type="click", value=[3, 4])
        self.assertEqual(points, [(3, 4)])
        self.as_plugin("plugin.a", lambda: window.draw(canvas, [ui.line(0, 0, 5, 5, "#00ff00")]))
        command = self.commands_list()[-1]
        self.assertEqual(command["method"], "ui.update")
        self.assertEqual(command["props"]["commands"][0]["op"], "line")

    def test_foreign_node_is_rejected(self):
        dialog = self.as_plugin("plugin.a", lambda: ui.show_dialog("x"))
        with self.assertRaises(ValueError):
            self.as_plugin("plugin.a", lambda: dialog.update(ui.Text("other"), text="y"))

    def test_unload_closes_plugin_surfaces_and_tells_the_client(self):
        dialog = self.as_plugin("plugin.a", lambda: ui.show_dialog("x"))
        other = self.as_plugin("plugin.b", lambda: ui.show_dialog("y"))
        self.commands_list()
        self.manager.disable("plugin.a")
        self.assertTrue(dialog.closed)
        self.assertFalse(other.closed)
        sent = self.commands_list()
        self.assertIn({"method": "ui.close_plugin", "plugin_id": "plugin.a"},
                      [{"method": item["method"], "plugin_id": item["plugin_id"]} for item in sent])
        self.manager.enable("plugin.a")
        self.assertEqual([key for key, value in self.runtime.surfaces.items()
                          if value.owner.plugin_id == "plugin.a"], [])

    def test_background_thread_can_show_and_callbacks_stay_on_dispatch_thread(self):
        threads = []
        button = ui.Button("x", on_click=lambda: threads.append(threading.get_ident()))
        result = {}

        def background():
            result["dialog"] = self.as_plugin("plugin.a", lambda: ui.show_dialog(button))

        worker = threading.Thread(target=background)
        worker.start()
        worker.join()
        dialog = result["dialog"]
        self.assertEqual(self.commands_list()[-1]["object_id"], dialog.id)
        self.event(plugin_id="plugin.a", object_id=dialog.id, node_id=button.id, type="click")
        self.assertEqual(threads, [threading.get_ident()])

    def test_unloaded_plugin_cannot_create_ui(self):
        owner = self.owners["plugin.a"]
        self.manager.disable("plugin.a")
        token = _current.set(owner)
        try:
            with self.assertRaises(RuntimeError):
                ui.show_dialog("x")
        finally:
            _current.reset(token)

    def test_example_plugin_shows_window_and_redraws_on_click(self):
        example = ROOT / "tools/ovygram/examples/ui_widgets.plugin"
        plugin_id = self.manager.install(str(example))
        self.commands_list()
        self.manager.enable(plugin_id)
        show = [item for item in self.commands_list() if item["method"] == "ui.show"]
        self.assertEqual([item["kind"] for item in show], ["window"])
        window = next(iter(value for value in self.runtime.surfaces.values()
                           if value.owner.plugin_id == plugin_id))
        canvas = next(node for node in window.nodes.values() if isinstance(node, ui.Canvas))
        self.event(plugin_id=plugin_id, object_id=window.id, node_id=canvas.id, type="click", value=[20, 30])
        update = self.commands_list()[-1]
        self.assertEqual(update["method"], "ui.update")
        self.assertIn({"op": "ellipse", "x": 15, "y": 25, "width": 10, "height": 10, "color": "#4fc3f7"},
                      update["props"]["commands"])
        self.assertNotIn(plugin_id, self.manager.errors)
        self.manager.disable(plugin_id)
        self.assertTrue(window.closed)

    def native_chat(self, account="42", chat_id=777, name="Друзья"):
        return {"account_id": account, "id": str(chat_id), "name": name, "kind": "chat",
                "input_peer": base64.b64encode(tl.encode(tl.inputPeerSelf())).decode("ascii")}

    def test_chat_bar_carries_account_and_chat(self):
        from desktop.models import chat_from_native
        chat = chat_from_native(self.native_chat())
        bar = self.as_plugin("plugin.a", lambda: ui.ChatBar(chat, ui.Text("x")).show())
        command = self.commands_list()[-1]
        self.assertEqual((command["kind"], command["account_id"], command["chat_id"]), ("chat_bar", "42", "777"))
        self.assertEqual(command["object_id"], bar.id)
        with self.assertRaises(TypeError):
            self.as_plugin("plugin.a", lambda: ui.ChatBar("777", ui.Text("x")))

    def test_chat_bar_example_follows_chat_and_counts_its_messages(self):
        plugin_id = self.manager.install(str(ROOT / "tools/ovygram/examples/chat_bar.plugin"))
        self.manager.enable(plugin_id)
        self.commands_list()
        self.runtime.native_event({"point": "chat_changed", "account_id": "42", "chat": self.native_chat()})
        shown = [item for item in self.commands_list() if item["method"] == "ui.show"]
        self.assertEqual([(item["kind"], item["chat_id"]) for item in shown], [("chat_bar", "777")])
        bar = self.runtime.surfaces[shown[0]["object_id"]]
        counter = next(node for node in bar.nodes.values() if isinstance(node, ui.Text))
        for account, chat_id in (("42", 777), ("43", 777), ("42", 5)):
            self.runtime.emit("new_message", Event(account, Message(account, 1, chat_id, "hi", 0, False)))
        updates = [item for item in self.commands_list() if item["method"] == "ui.update"]
        self.assertEqual([item["props"]["text"] for item in updates], ["🧩 Друзья: новых сообщений 1"])
        self.assertEqual(updates[0]["node_id"], counter.id)
        self.runtime.native_event({"point": "chat_changed", "account_id": "42", "chat": self.native_chat(chat_id=5, name="Другой")})
        sent = self.commands_list()
        self.assertEqual([item["method"] for item in sent if item["method"].startswith("ui.")], ["ui.close", "ui.show"])
        self.assertNotIn(plugin_id, self.manager.errors)

    def test_layout_options_are_sent_and_validated(self):
        tree = ui.Row(ui.Text("a", align="center", stretch=2), ui.Button("b", width="fit"),
                      ui.Spacer(4, width=12), align="bottom", spacing=4).to_json()
        self.assertEqual((tree["align"], tree["spacing"]), ("bottom", 4))
        self.assertEqual([(child.get("width"), child.get("stretch")) for child in tree["children"]],
                         [(None, 2), ("fit", None), (12, None)])
        self.assertEqual(tree["children"][0]["align"], "center")
        self.assertEqual(ui.Row().to_json()["align"], "center")
        for bad in (lambda: ui.Row(align="middle"), lambda: ui.Text("x", align="justify"),
                    lambda: ui.Button("x", width="auto"), lambda: ui.Button("x", width=-1),
                    lambda: ui.Text("x", stretch=101), lambda: ui.Row(spacing=-1)):
            with self.assertRaises(ValueError):
                bad()

    def test_elements_send_rules_route_clicks_and_clean_up(self):
        clicks = []
        call = self.as_plugin("plugin.a", lambda: ui.element("chat.top_bar.call"))
        self.as_plugin("plugin.a", call.hide)
        self.as_plugin("plugin.a", lambda: call.on_click(lambda: clicks.append(1), replace=True))
        sent = [(item["method"], item.get("hidden"), item.get("replace")) for item in self.commands_list()]
        self.assertEqual(sent, [("ui.element.hide", True, None), ("ui.element.click", None, True)])
        self.event(plugin_id="plugin.a", type="element_click", element="chat.top_bar.call")
        self.event(plugin_id="plugin.b", type="element_click", element="chat.top_bar.call")
        self.assertEqual(clicks, [1])
        with self.assertRaises(ValueError):
            self.as_plugin("plugin.a", lambda: ui.element("chat.top_bar.unknown"))
        self.manager.disable("plugin.a")
        self.assertEqual(self.runtime.element_handlers, {})

    def test_palette_commands_and_errors_without_surface(self):
        self.as_plugin("plugin.a", lambda: ui.set_colors({"windowBg": "#101820"}))
        self.as_plugin("plugin.a", ui.reset_colors)
        sent = self.commands_list()
        self.assertEqual([(item["method"], item.get("colors"), item.get("reset")) for item in sent],
                         [("ui.palette", {"windowBg": "#101820"}, None), ("ui.palette", None, True)])
        with self.assertRaises(ValueError):
            self.as_plugin("plugin.a", lambda: ui.set_colors({"windowBg": "red"}))
        self.event(plugin_id="plugin.a", type="error", value="Unknown palette color: x")
        self.assertEqual(self.manager.errors["plugin.a"], "Unknown palette color: x")

    def test_top_bar_example_hides_call_by_default(self):
        plugin_id = self.manager.install(str(ROOT / "tools/ovygram/examples/top_bar.plugin"))
        self.commands_list()
        self.manager.enable(plugin_id)
        methods = [(item["method"], item.get("element"), item.get("hidden")) for item in self.commands_list()]
        self.assertIn(("ui.element.hide", "chat.top_bar.call", True), methods)
        self.assertNotIn(plugin_id, self.manager.errors)

    def test_widget_rules_keys_and_cleanup(self):
        clicks, keys = [], []
        hide = self.as_plugin("plugin.a", lambda: ui.hide_widgets(
            cls="Ui::IconButton", ancestor="HistoryView::TopBarWidget", index=1))
        click = self.as_plugin("plugin.a", lambda: ui.on_widget_click(
            lambda: clicks.append(1), replace=True, accessible="Call"))
        key = self.as_plugin("plugin.a", lambda: ui.on_key("Ctrl+Shift+K", lambda: keys.append(1)))
        sent = self.commands_list()
        self.assertEqual([item["method"] for item in sent], ["ui.widgets.rule", "ui.widgets.rule", "ui.keys.add"])
        self.assertEqual(sent[0]["selector"], {"cls": "Ui::IconButton",
                                               "ancestor": "HistoryView::TopBarWidget", "index": 1})
        self.assertEqual((sent[1]["action"], sent[1]["replace"]), ("click", True))
        self.event(plugin_id="plugin.a", type="widget_click", rule_id=click.id)
        self.event(plugin_id="plugin.b", type="widget_click", rule_id=click.id)
        self.event(plugin_id="plugin.a", type="key", rule_id=key.id)
        self.assertEqual((clicks, keys), ([1], [1]))
        self.as_plugin("plugin.a", hide.remove)
        last = self.commands_list()[-1]
        self.assertEqual((last["method"], last["rule_id"]), ("ui.widgets.unrule", hide.id))
        self.manager.disable("plugin.a")
        self.assertEqual(self.runtime.widget_rules, {})

    def test_selector_validation(self):
        for bad in (lambda: ui.hide_widgets(), lambda: ui.hide_widgets(index=1),
                    lambda: ui.hide_widgets(cls="X", color="red"), lambda: ui.hide_widgets(cls="X", index=-1),
                    lambda: ui.on_key("", lambda: None), lambda: ui.Overlay("abc", ui.Canvas(10))):
            with self.assertRaises(ValueError):
                self.as_plugin("plugin.a", bad)

    def test_overlay_and_tree_requests(self):
        canvas = ui.Canvas(20, on_click=lambda x, y: None)
        overlay = self.as_plugin("plugin.a", lambda: ui.Overlay({"handle": "17"}, canvas).show())
        command = self.commands_list()[-1]
        self.assertEqual((command["kind"], command["target"], command["clickable"]), ("overlay", "17", True))
        self.assertEqual(command["object_id"], overlay.id)

        async def tree():
            return await ui.widget_tree(depth=3)

        future = self.runtime.schedule(self.owners["plugin.a"], tree())
        request = self.commands.get(timeout=2)
        self.assertEqual((request["method"], request["depth"], request["root"]), ("widgets.tree", 3, None))
        self.runtime.complete({"id": request["id"], "result": {"handle": "1", "cls": "Window"}})
        self.assertEqual(future.result(timeout=2)["cls"], "Window")

    def test_clipboard_command(self):
        self.as_plugin("plugin.a", lambda: ui.set_clipboard("дерево"))
        command = self.commands_list()[-1]
        self.assertEqual((command["method"], command["text"]), ("ui.clipboard", "дерево"))

    def test_chat_decorations(self):
        from desktop.models import chat_from_native
        chat = chat_from_native(self.native_chat())
        mark = self.as_plugin("plugin.a", lambda: ui.decorate_chat(
            chat, [ui.ellipse(-22, 10, 10, 10, "#00bcd4")], background="#1500bcd4"))
        command = self.commands_list()[-1]
        self.assertEqual((command["method"], command["account_id"], command["chat_id"], command["background"]),
                         ("ui.decoration.set", "42", "777", "#1500bcd4"))
        self.assertEqual(command["commands"][0]["x"], -22)
        self.as_plugin("plugin.a", lambda: mark.update([], background=None))
        self.as_plugin("plugin.a", mark.remove)
        self.assertEqual([item["method"] for item in self.commands_list()],
                         ["ui.decoration.set", "ui.decoration.remove"])
        every = self.as_plugin("plugin.a", lambda: ui.decorate_chat("*", account="42"))
        self.assertEqual(self.commands_list()[-1]["chat_id"], "*")
        for bad in (lambda: ui.decorate_chat("*"), lambda: ui.decorate_chat("777"),
                    lambda: ui.decorate_chat(chat, background="red")):
            with self.assertRaises((ValueError, TypeError)):
                self.as_plugin("plugin.a", bad)

    def test_compose_field_api(self):
        self.as_plugin("plugin.a", lambda: ui.set_compose_text("Привет"))
        self.as_plugin("plugin.a", lambda: ui.insert_compose_text("!"))
        self.assertEqual([(item["method"], item["text"]) for item in self.commands_list()],
                         [("ui.compose.set", "Привет"), ("ui.compose.insert", "!")])
        self.as_plugin("plugin.a", lambda: ui.element("compose.emoji").hide())

        async def read():
            return await ui.compose_text()

        future = self.runtime.schedule(self.owners["plugin.a"], read())
        while True:
            request = self.commands.get(timeout=2)
            if request["method"] == "compose.get_text":
                break
        self.runtime.complete({"id": request["id"], "result": "текст"})
        self.assertEqual(future.result(timeout=2), "текст")

    def test_chat_style_example_loads(self):
        plugin_id = self.manager.install(str(ROOT / "tools/ovygram/examples/chat_style.plugin"))
        self.commands_list()
        self.manager.enable(plugin_id)
        methods = [item["method"] for item in self.commands_list()]
        self.assertIn("ui.element.hide", methods)
        self.assertIn("ui.keys.add", methods)
        self.runtime.native_event({"point": "chat_changed", "account_id": "42", "chat": self.native_chat()})
        self.assertEqual(self.commands_list()[-1]["method"], "ui.decoration.set")
        self.assertNotIn(plugin_id, self.manager.errors)

    def test_menu_item_click_gets_chat_and_message(self):
        clicks = []
        item = self.as_plugin("plugin.a", lambda: ui.add_menu_item(
            "message", "Скопировать", clicks.append, kinds=["user", "chat"]))
        command = self.commands_list()[-1]
        self.assertEqual((command["method"], command["menu"], command["text"], command["kinds"]),
                         ("ui.menu.add", "message", "Скопировать", ["user", "chat"]))
        self.event(plugin_id="plugin.a", type="menu_click", rule_id=command["rule_id"], value={
            "account_id": "42", "chat": self.native_chat(),
            "message": {"account_id": "42", "id": "9", "chat_id": "777", "text": "привет",
                        "date": 0, "outgoing": False}})
        self.assertEqual(len(clicks), 1)
        menu = clicks[0]
        self.assertEqual((menu.account_id, menu.chat.id, menu.message.id, menu.message.text),
                         ("42", 777, 9, "привет"))
        self.as_plugin("plugin.a", item.remove)
        self.assertEqual([item["method"] for item in self.commands_list()], ["ui.menu.remove"])
        self.event(plugin_id="plugin.a", type="menu_click", rule_id=command["rule_id"],
                   value={"account_id": "42"})
        self.assertEqual(len(clicks), 1)

    def test_main_menu_item_and_validation(self):
        clicks = []
        self.as_plugin("plugin.a", lambda: ui.add_menu_item("main", "Сводка", clicks.append))
        command = self.commands_list()[-1]
        self.event(plugin_id="plugin.a", type="menu_click", rule_id=command["rule_id"],
                   value={"account_id": "42"})
        self.assertEqual((clicks[0].account_id, clicks[0].chat, clicks[0].message), ("42", None, None))
        for arguments in (("sidebar", "x"), ("main", ""), ("main", "x" * 65)):
            with self.assertRaises(ValueError):
                self.as_plugin("plugin.a", lambda: ui.add_menu_item(*arguments, print))
        with self.assertRaises(ValueError):
            self.as_plugin("plugin.a", lambda: ui.add_menu_item("main", "x", print, kinds=["user"]))
        with self.assertRaises(ValueError):
            self.as_plugin("plugin.a", lambda: ui.add_menu_item("chat", "x", print, kinds=["bot"]))

    def test_menus_example_registers_its_items(self):
        plugin_id = self.manager.install(str(ROOT / "tools/ovygram/examples/menus.plugin"))
        self.manager.enable(plugin_id)
        menus = [item["menu"] for item in self.commands_list() if item["method"] == "ui.menu.add"]
        self.assertEqual(menus, ["main", "chat", "message", "message"])
        self.manager.disable(plugin_id)
        self.assertIn("ui.close_plugin", [item["method"] for item in self.commands_list()])

    def test_section_is_shown_and_closed_by_the_window(self):
        closed = []
        section = self.as_plugin("plugin.a", lambda: ui.Section(
            ui.Column(ui.Text("x")), title="Страница", on_close=lambda: closed.append(True)).show())
        command = self.commands_list()[-1]
        self.assertEqual((command["method"], command["kind"], command["title"]),
                         ("ui.show", "section", "Страница"))
        # The window history dropped the section.
        self.event(plugin_id="plugin.a", object_id=section.id, type="closed")
        self.assertTrue(section.closed)
        self.assertEqual(closed, [True])
        with self.assertRaises(ui.ObjectDestroyed):
            section.update(section.content.children[0], text="y")

    def test_section_example_opens_from_the_main_menu(self):
        plugin_id = self.manager.install(str(ROOT / "tools/ovygram/examples/section.plugin"))
        self.manager.enable(plugin_id)
        menus = [item for item in self.commands_list() if item["method"] == "ui.menu.add"]
        self.assertEqual([item["menu"] for item in menus], ["main"])

    def test_native_window_events_and_signals(self):
        from desktop import native
        windows, titles = [], []
        watch = self.as_plugin("plugin.a", lambda: native.on_window(windows.append))
        command = self.commands_list()[-1]
        self.assertEqual((command["method"], command["enabled"]), ("ui.native.windows", True))
        event = {"event": "shown", "handle": "5", "cls": "Ui::PopupMenu", "kind": "popup", "title": ""}
        self.event(plugin_id="plugin.a", type="native_window", rule_id=command["rule_id"], value=event)
        self.assertEqual(windows, [event])
        connection = self.as_plugin("plugin.a", lambda: native.connect(
            {"handle": "7"}, "windowTitleChanged", titles.append))
        command = self.commands_list()[-1]
        self.assertEqual((command["method"], command["handle"], command["signal"]),
                         ("ui.native.connect", "7", "windowTitleChanged"))
        self.event(plugin_id="plugin.a", type="native_signal", rule_id=command["rule_id"],
                   value=["Telegram (3)"])
        self.assertEqual(titles, ["Telegram (3)"])
        self.as_plugin("plugin.a", watch.remove)
        self.as_plugin("plugin.a", connection.remove)
        self.assertEqual([item["method"] for item in self.commands_list()],
                         ["ui.native.disconnect", "ui.native.disconnect"])

    def test_native_invoke_sends_a_request(self):
        from desktop import native
        future = self.runtime.schedule(self.owners["plugin.a"],
                                       native.invoke("12", "setWindowTitle", "x"))
        request = self.wait_for("native.invoke")[0]
        self.assertEqual((request["handle"], request["name"], request["args"]),
                         ("12", "setWindowTitle", ["x"]))
        self.runtime.complete({"id": request["id"], "result": None})
        self.assertIsNone(future.result(timeout=2))

    def test_native_example_watches_windows(self):
        plugin_id = self.manager.install(str(ROOT / "tools/ovygram/examples/native_events.plugin"))
        self.manager.enable(plugin_id)
        methods = {item["method"] for item in self.commands_list()}
        self.assertTrue({"ui.native.windows", "ui.keys.add"} <= methods)
        self.manager.disable(plugin_id)

    def load_math(self):
        plugin_id = self.manager.install(str(ROOT / "tools/ovygram/examples/math_autocomplete.plugin"))
        self.manager.enable(plugin_id)
        watch = [item for item in self.commands_list() if item["method"] == "ui.compose.watch"]
        self.assertEqual(len(watch), 1)
        instance = self.manager.loaded[plugin_id][0]
        return plugin_id, instance, watch[0]["rule_id"]

    def change(self, plugin_id, rule_id, text, cursor, selection=None):
        start, end = selection or (cursor, cursor)
        self.event(plugin_id=plugin_id, type="compose_changed", rule_id=rule_id,
                   value={"text": text, "cursor": cursor, "selection_start": start, "selection_end": end})

    def answer_state(self, text, cursor, selection=None):
        start, end = selection or (cursor, cursor)
        while True:
            request = self.commands.get(timeout=2)
            if request["method"] == "compose.get_state":
                break
        self.runtime.complete({"id": request["id"], "result": {
            "text": text, "cursor": cursor, "selection_start": start, "selection_end": end}})

    def wait_for(self, method):
        for _ in range(200):
            items = [item for item in self.commands_list() if item["method"] == method]
            if items:
                return items
            __import__("time").sleep(0.01)
        self.fail(f"{method} was not sent")

    def test_math_evaluation(self):
        namespace = {}
        source = (ROOT / "tools/ovygram/examples/math_autocomplete.plugin").read_text(encoding="utf-8")
        exec(compile(source.split("class MathAutocompletePlugin")[0].replace(
            "from base_plugin import BasePlugin\nfrom desktop import ui\n", ""), "math", "exec"), namespace)
        evaluate = namespace["evaluate"]
        self.assertEqual(evaluate("1+3"), "4")
        self.assertEqual(evaluate("2*(3+4)"), "14")
        self.assertEqual(evaluate("7/2"), "3.5")
        self.assertEqual(evaluate("1,5*2"), "3")
        self.assertEqual(evaluate("-2**3"), "-8")
        for bad in ("5", "__import__('os')", "2**1000", "a+1"):
            with self.assertRaises((ValueError, SyntaxError)):
                evaluate(bad)

    def test_math_suggestion_accept_and_backspace(self):
        plugin_id, instance, rule_id = self.load_math()
        self.change(plugin_id, rule_id, "1+3=", 4)
        sent = self.commands_list()
        replace = [item for item in sent if item["method"] == "ui.compose.replace"][0]
        self.assertEqual((replace["start"], replace["end"], replace["text"], replace["select"]), (4, 4, "4", True))
        space = [item for item in sent if item["method"] == "ui.keys.add"][0]
        self.assertEqual((space["sequence"], space["element"], space["replace"]), ("Space", "compose.field", True))
        # The client doesn't report the plugin's own edits back.
        self.assertEqual(instance.suggestion, (4, 5))
        self.event(plugin_id=plugin_id, type="key", rule_id=space["rule_id"])
        self.answer_state("1+3=4", 5, (4, 5))
        accept = self.wait_for("ui.compose.replace")[0]
        self.assertEqual((accept["start"], accept["end"], accept["text"]), (5, 5, " "))
        self.assertEqual(instance.accepted, (4, 6))
        backspace = [item for item in self.commands_list() if item["method"] == "ui.keys.add"]
        self.assertIsNotNone(instance.backspace_rule)
        self.event(plugin_id=plugin_id, type="key", rule_id=instance.backspace_rule.id)
        self.answer_state("1+3=4 ", 6)
        removal = self.wait_for("ui.compose.replace")[0]
        self.assertEqual((removal["start"], removal["end"], removal["text"]), (4, 6, ""))
        self.assertNotIn(plugin_id, self.manager.errors)

    def test_math_suggestion_dropped_by_typing(self):
        plugin_id, instance, rule_id = self.load_math()
        self.change(plugin_id, rule_id, "2*5=", 4)
        self.assertEqual(instance.suggestion, (4, 6))
        self.change(plugin_id, rule_id, "2*5=x", 5)  # A typed char replaced the selection.
        self.assertIsNone(instance.suggestion)
        self.assertIn("ui.widgets.unrule", [item["method"] for item in self.commands_list()])

    def test_hide_chats_and_message_decorations(self):
        from desktop.models import chat_from_native
        first = chat_from_native(self.native_chat("42", 777))
        second = chat_from_native(self.native_chat("43", 5))
        hidden = self.as_plugin("plugin.a", lambda: ui.hide_chats([first, second]))
        sent = sorted((item["account_id"], tuple(item["chat_ids"])) for item in self.commands_list())
        self.assertEqual(sent, [("42", ("777",)), ("43", ("5",))])
        self.as_plugin("plugin.a", hidden.remove)
        self.assertEqual({item["method"] for item in self.commands_list()}, {"ui.chat_list.unhide"})
        with self.assertRaises(ValueError):
            self.as_plugin("plugin.a", lambda: ui.hide_chats([]))
        message = Message("42", 9, 777, "text", 0, False)
        mark = self.as_plugin("plugin.a", lambda: ui.decorate_message(
            message, [ui.text(-58, 16, "★", "#ff9800")], background="#22ff9800"))
        command = self.commands_list()[-1]
        self.assertEqual((command["method"], command["chat_id"], command["message_id"]),
                         ("ui.message_decoration.set", "777", 9))
        self.as_plugin("plugin.a", mark.remove)
        self.assertEqual(self.commands_list()[-1]["method"], "ui.message_decoration.remove")

    def test_highlight_example(self):
        plugin_id = self.manager.install(str(ROOT / "tools/ovygram/examples/highlight.plugin"))
        self.manager.enable(plugin_id)
        self.commands_list()
        self.runtime.emit("new_message", Event("42", Message("42", 3, 777, "Привет, Ovygram!", 0, False)))
        self.runtime.emit("new_message", Event("42", Message("42", 4, 777, "без слова", 0, False)))
        sent = [item for item in self.commands_list() if item["method"] == "ui.message_decoration.set"]
        self.assertEqual([item["message_id"] for item in sent], [3])
        self.assertNotIn(plugin_id, self.manager.errors)


if __name__ == "__main__":
    unittest.main()
