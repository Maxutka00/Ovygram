from base_plugin import BasePlugin
from desktop import client, ui
from desktop_utils import run_on_ui

__id__ = "chat_bar"
__name__ = "Полоса в чате"
__version__ = "1.0.0"
__release__ = False
__author__ = "Ovygram"
__description__ = "Полоса над сообщениями открытого чата со счётчиком и кнопками."
__platform__ = "desktop"
__desktop_sdk__ = 2
__requirements__ = []


class ChatBarPlugin(BasePlugin):
    def on_plugin_load(self):
        self.bar = None
        self.chat = None
        self.count = 0
        self.counter = None
        self.subscribe("chat_changed", self.on_chat)
        self.subscribe("new_message", self.on_message)
        self.run_async(self.show_for_current_chat())

    async def show_for_current_chat(self):
        for account in await client.accounts():
            if account.active:
                chat = await client.current_chat(account.id)
                if chat is not None:
                    await run_on_ui(lambda: self.show_bar(chat))
                return

    def on_chat(self, event):
        self.show_bar(event.chat)

    def show_bar(self, chat):
        if self.bar is not None:
            self.bar.close()
            self.bar = None
        self.chat = chat
        self.count = 0
        if chat is None:
            return
        self.counter = ui.Text(self.label())
        self.bar = ui.ChatBar(
            chat,
            ui.Row(
                self.counter,
                ui.Button("Поздороваться", on_click=self.greet),
                ui.Button("Скрыть", on_click=self.hide),
            ),
        ).show()

    def label(self):
        return f"🧩 {self.chat.name}: новых сообщений {self.count}"

    def on_message(self, event):
        chat = self.chat
        if (self.bar is None or self.bar.closed or chat is None
                or event.account_id != chat.account_id or event.message.chat_id != chat.id):
            return
        self.count += 1
        self.bar.update(self.counter, text=self.label())

    def greet(self):
        if self.chat is not None:
            self.run_async(client.send_message(self.chat, "Привет 👋"))

    def hide(self):
        if self.bar is not None:
            self.bar.close()
