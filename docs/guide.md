# Руководство по плагинам Ovygram

Плагины Ovygram — код на Python 3.13, который работает внутри клиента.
Они получают события Telegram, отправляют сообщения и запросы, меняют
отправляемое и полученное через хуки и добавляют свой интерфейс.

Плагины не изолированы: у них те же права, что у клиента. Включайте только
плагины, которым доверяете.

Подробные справочники: [SDK](sdk.md), [интерфейс](ui.md),
[точки перехвата](hooks.md), [зависимости](dependencies.md),
[управление плагинами](plugins.md), [перенос Android-плагинов](porting-android.md).

## Первый плагин

Создайте файл `hello.plugin`:

```python
from base_plugin import BasePlugin

__id__ = "yourname.hello"
__name__ = "Привет"
__version__ = "1.0.0"
__author__ = "Вы"
__description__ = "Пишет в журнал при запуске."
__platform__ = "desktop"
__desktop_sdk__ = 2


class HelloPlugin(BasePlugin):
    def on_plugin_load(self):
        self.log("Привет из плагина")

    def on_plugin_unload(self):
        self.log("Пока")
```

«Настройки → Плагины → Импортировать плагин», выберите файл и включите
плагин. Сообщение появится в журнале («Открыть журнал» внизу страницы).

- Метаданные читаются без запуска кода, поэтому это должны быть простые
  строки и числа. `__id__` — строчные буквы, цифры, `.`, `_`, `-`.
- В файле один класс-наследник `BasePlugin`.
- После правок — «Обновить из файла» на странице плагина.
- Проект из нескольких файлов — ZIP с `plugin.json`; готовый
  [шаблон](../tools/ovygram/template) с автодополнением и сборкой архива.

## События

```python
def on_plugin_load(self):
    self.subscribe("new_message", self.on_message)

async def on_message(self, event):
    self.log(f"{event.chat_id}: {event.message.text}")
```

События: `new_message`, `edited_message`, `deleted_message`,
`account_changed`, `accounts_changed`, `chat_changed`. Синхронный
обработчик выполняется в главном потоке, `async def` — в отдельном цикле
`asyncio`. Подробно — [SDK: события](sdk.md#события).

## Сообщения и запросы

```python
from desktop import client, tl

async def reply(self, chat):
    await client.send_message(chat, "Готово")
    state = await client.rpc(chat.account_id, tl.updates.getState())
```

Все операции асинхронные и явно привязаны к аккаунту: у `Chat`, `Message`
и других объектов есть `account_id`. Из синхронного кода запускайте их
через `self.run_async(...)`. Любой метод Telegram API доступен как
TL-объект `desktop.tl`. Подробно — [SDK: операции](sdk.md#доступные-операции),
файлы — [SDK: файлы](sdk.md#файлы).

## Настройки

```python
from ui.settings import Input, Selector, Switch

def create_settings(self):
    return [
        Switch("enabled", "Отвечать автоматически", True),
        Input("text", "Текст ответа", "Я занят"),
        Selector("mode", "Режим", ["Всем", "Только контактам"], 0),
    ]

def on_message(self, event):
    if self.get_setting("enabled", True):
        ...
```

Страница плагина в настройках клиента показывает эти поля, кнопка
«Сохранить настройки» записывает их. Значения доступны через
`get_setting` / `set_setting`, раздельно по аккаунтам — через
`get_account_setting` / `set_account_setting`. Настройки сохраняются при
обновлении и откате плагина. Файлы плагина храните в
`file_utils.get_plugin_data_dir()`.

## Интерфейс

```python
from desktop import ui

def on_plugin_load(self):
    ui.add_menu_item("message", "Скопировать текст",
                     lambda menu: ui.set_clipboard(menu.message.text))

def show(self):
    ui.show_dialog(ui.Column(ui.Text("Привет"), ui.Button("OK")), title="Плагин")
```

Свои диалоги, окна, страницы в основной колонке, полосы над сообщениями
чата и холсты; пункты в меню Telegram; скрытие и перехват встроенных
кнопок; сочетания клавиш; работа со строкой ввода; декорации списка чатов
и сообщений; цвета темы. Всё — в [`desktop.ui`](ui.md); для Qt-сигналов и
окон — `desktop.native`.

## Хуки

```python
from hook_utils import MODIFY, HookResult

def on_plugin_load(self):
    self.add_hook("before_send", self.shout, request="messages.sendMessage")

def shout(self, message):
    message.text = message.text.upper()
    return HookResult(MODIFY, message)
```

Точки: `before_send`, `before_rpc`, `after_rpc`, `before_updates`. Хуки
синхронные, выполняются в главном потоке и должны быть быстрыми.
`CANCEL` отменяет операцию. Подробно — [SDK: хуки](sdk.md#хуки), все точки
перехвата — в [справочнике](hooks.md).

## Зависимости

```python
__requirements__ = ["requests>=2.31,<3"]
```

Клиент ставит библиотеки с PyPI при включении плагина и запускает его
после установки. Только готовые wheels; конфликты версий показываются на
карточке плагина. Подробно — [зависимости](dependencies.md).

## Отладка

- **Журнал.** `self.log(...)` и ошибки плагинов пишутся в `plugins.log` в
  каталоге профиля; кнопка «Открыть журнал» на странице плагинов.
- **Ошибки.** Исключение в `on_plugin_load`, обработчике или хуке
  показывается на карточке плагина. Ошибка в хуке отправки отменяет
  отправку с уведомлением; ошибка в `after_rpc` и `before_updates` не мешает
  клиенту.
- **Обновление без перезапуска.** «Обновить из файла» выгружает старую
  версию и снимает всё, что она зарегистрировала; новая версия ждёт
  включения. «Откатить» возвращает предыдущую.
- **Интерфейс Telegram.** Пример
  [`widget_inspector`](../tools/ovygram/examples/widget_inspector.plugin)
  показывает дерево виджетов по Ctrl+Shift+I — так находятся классы и имена
  для `hide_widgets` и `desktop.native`.
- **Сбой клиента.** Если клиент упал, при следующем запуске плагины не
  запустятся до кнопки «Возобновить запуск плагинов». Параметр запуска
  `--disable-plugins` отключает плагины совсем.
- **Зависание.** Код плагина работает в процессе клиента: бесконечный цикл
  в главном потоке подвесит окно. Долгую работу выносите в `async def` или
  `desktop_utils.run_in_background`.
- **Тесты.** SDK можно импортировать вне клиента: добавьте
  `Telegram/PluginSDK` в `sys.path` и проверяйте свою логику обычными
  тестами; примеры — в `tools/ovygram/tests`.

## Примеры

В [`tools/ovygram/examples`](../tools/ovygram/examples) лежат рабочие
плагины — от курсов валют, погоды и RSS до статистики чата и напоминаний.
[Список с описанием](../tools/ovygram/examples/README.md) показывает, какой
приём демонстрирует каждый, и правила, которым они следуют.
