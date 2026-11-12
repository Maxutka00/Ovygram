from base_plugin import BasePlugin
from desktop import ui
from ui.settings import Input, Switch

from .helpers import greeting

# Metadata is read without running the code, so it must be plain literals.
__id__ = "example_template"  # Latin letters, digits and _, up to 25: e.g. "yourname_weather".
__name__ = "Шаблон плагина"
__version__ = "1.0.0"  # Numbers with dots, a suffix after a dot: 1.2, 1.2b.
__release__ = False  # True: public, published to the plugin repository after review.
__author__ = "Автор"
__description__ = "Отвечает на новые сообщения в журнал и добавляет пункт в меню сообщения."
__platform__ = "desktop"
__desktop_sdk__ = 2
__requirements__ = []  # PyPI libraries, e.g. ["requests>=2.31"], see docs/dependencies.md.


class TemplatePlugin(BasePlugin):
    def on_plugin_load(self):
        # Everything registered here is removed when the plugin is unloaded.
        self.subscribe("new_message", self.on_new_message)
        ui.add_menu_item("message", "Поприветствовать автора", self.on_greet)
        self.log("Шаблон загружен")

    def on_plugin_unload(self):
        self.log("Шаблон выгружен")

    def create_settings(self):
        return [
            Input("name", "Имя в приветствии", "мир"),
            Switch("excited", "С восклицательным знаком", True),
        ]

    async def on_new_message(self, event):
        # async handlers run in the plugin's asyncio loop, off the UI thread.
        if not event.message.outgoing:
            self.log(f"Новое сообщение в чате {event.chat_id}: {event.message.text[:50]!r}")

    def on_greet(self, menu):
        text = greeting(self.get_setting("name", "мир"), self.get_setting("excited", True))
        ui.insert_compose_text(text + " ")
