# SDK аккаунтов, сообщений и хуков

Эти API подготовлены в исходниках этапа 3 на основе Telegram Desktop v7.3.5.
Локальные тесты проверяют Python SDK и его обмен с моделью клиента. Компиляция
C++ интеграции и проверка в Telegram-сеансе выполняются следующим шагом после
отдельного указания пользователя запустить сборку.

## Первый асинхронный запрос

```python
from base_plugin import BasePlugin
from desktop import client, tl

class ExamplePlugin(BasePlugin):
    def on_plugin_load(self):
        self.run_async(self.show_accounts())

    async def show_accounts(self):
        for account in await client.accounts():
            state = await client.rpc(account, tl.updates.getState())
            self.log(f"Аккаунт {account.id}, pts={state.pts}")
```

Добавь обязательные метаданные из [примера аккаунтов](../tools/ovygram/examples/account_events.ovyplugin).
Для новых API укажи `__desktop_sdk__ = 2`. Плагины SDK 1 продолжают
поддерживаться. Ранее выпущенный клиент с SDK 1 отклонит импорт SDK 2.
Плагин после импорта включается вручную. Вызовы идут через существующие сессии
клиента. У каждого запроса явно указан аккаунт, у `Chat`, `Message`, `User`,
`Attachment`, `Event` и `Progress` есть `account_id`.

`Account.id` — строковое значение `Main::Session::uniqueId()`. `Chat.id` использует
представление `PeerId` этого клиента. Получай его из событий и `get_chat`, сохраняя
сопровождающий ID аккаунта. Для самостоятельно созданных TL-запросов используются
обычные поля TL-схемы, включая `InputPeer` и `access_hash`.

## Доступные операции

| Python-метод | Результат и поведение |
| --- | --- |
| `await client.accounts()` | Список `Account` открытых сессий |
| `await client.current_chat(account)` | `Chat` последнего активного окна этого аккаунта или `None` |
| `await client.get_chat(account, chat_id)` | Снимок загруженного чата с `input_peer` |
| `await client.get_user(account, user_id)` | Снимок загруженного пользователя |
| `await client.get_loaded_message(chat, message_id)` | Снимок загруженного сообщения или `None` |
| `await client.get_message(chat, message_id)` | Загрузка сообщения из Telegram |
| `await client.history(chat, limit=50, offset_id=0)` | Страница истории, до 100 сообщений |
| `await client.send_message(chat, text, reply_to=None, silent=False, no_webpage=False)` | Отправка текста, результат TL `Updates` |
| `await client.edit_message(chat, message_id, text)` | Изменение текста |
| `await client.delete_messages(chat, ids, revoke=True)` | Удаление сообщений |
| `await client.forward_messages(source, target, ids, silent=False)` | Пересылка между чатами одного аккаунта |
| `await client.rpc(account, request, dc_id=0, timeout=60)` | Типизированный TL-ответ или `RpcError` |

`get_chat` и `get_user` читают загруженные данные. Для разрешения новых
пользователей и чатов можно вызвать соответствующий TL-метод, например
`contacts.resolveUsername`. Поля TL-ответа доступны как атрибуты Python-объекта.
`History` и `get_message` обрабатывают возвращённые сообщения в модели клиента.

`client_utils` экспортирует те же функции и операции с файлами. Ошибка RPC
содержит `code`, `name`, `description`. Выход из аккаунта завершает ожидающие
запросы ошибкой `ACCOUNT_CLOSED`. Переключение окна не меняет аккаунт запроса.

## TL-типы

`desktop.tl` содержит 2578 конструкторов и методов из закреплённой `api.tl`.
Файл `__init__.pyi` предоставляет объявления для редактора. Поля передаются
именованными аргументами. Флаги вычисляются из необязательных полей.

```python
request = tl.messages.getHistory(
    peer=chat.input_peer,
    offset_id=0,
    offset_date=0,
    add_offset=0,
    limit=25,
    max_id=0,
    min_id=0,
    hash=0,
)
response = await client.rpc(chat.account_id, request)
```

Необязательное поле пропускается при `None`. Поле вида `flags.N?true`
включается значением `True`. Группа полей с одним битом должна задаваться
целиком. Python-ключевые слова и поле `self` получают суффикс `_`, например
`from_` и `self_`. `Bool` представлен `bool`, TL-байты представлены `bytes`.

`tl.encode` и `tl.decode` проверяют типы, длину, вложенность и остаток пакета.
Генератор `tools/ovygram/generate_tl.py` воспроизводит каталог и `.pyi`
по исходной схеме. Тест сравнивает каталог с закреплённой схемой.

## События

```python
def on_plugin_load(self):
    self.subscribe("new_message", self.new_message)

async def new_message(self, event):
    message = event.message
    self.log(f"Аккаунт {event.account_id}, сообщение {message.id}")
```

| Событие | Поля `Event` |
| --- | --- |
| `new_message` | `account_id`, `message`, `chat_id` |
| `edited_message` | `account_id`, `message`, `chat_id` |
| `deleted_message` | `account_id`, `message_ids`, для канала `chat_id` |
| `account_changed` | `account_id` активированного аккаунта |
| `accounts_changed` | `account_id` сессии, затронутой изменением списка |
| `chat_changed` | `account_id`, `chat` или `None` при закрытии чата |

Для удаления обычных сообщений Telegram передаёт ID без чата, поэтому
`chat_id` такого события равен `None`. Повтор одинакового обновления
отфильтровывается в пределах последних 2048 обновлений. Для новых сообщений
дополнительно запоминаются последние 2048 сочетаний аккаунта, чата и ID.
Догрузка новых сообщений через `getDifference` и `getChannelDifference`
доставляет те же события. Синхронный обработчик
вызывается на главном потоке. `async def` запускается в управляемом цикле.

## Хуки

```python
from hook_utils import MODIFY, HookResult

def on_plugin_load(self):
    self.add_hook("before_send", self.change_text,
                  request="messages.sendMessage", priority=10)

def change_text(self, message):
    message.text = message.text.upper()
    return HookResult(MODIFY, message)
```

| Точка | Аргумент | Действия |
| --- | --- | --- |
| `before_send` | `OutgoingMessage(account_id, request)` | Изменение текста, подписи, `InputMedia` и параметров либо отмена |
| `before_rpc` | `RpcContext(account_id, request_id, request)` | Изменение полей запроса либо отмена |
| `after_rpc` | `RpcResponse(account_id, request_id, response, error, request)` | Изменение TL-байтов ответа или описания ошибки, отмена обработки |
| `before_updates` | `UpdateContext(account_id, updates)` | Изменение пакета `Updates` или пропуск его обработки |

`OutgoingMessage.text` доступен для одиночного текста и подписи. При его
изменении прежние `entities` очищаются. Для альбома изменяй `request.multi_media`.
Состав `random_id` альбома сохраняется. Получатель и `random_id` отправки,
ID запроса и аккаунт сохраняются при изменении хуками. Для отправки в другой
чат вызывай отдельную операцию SDK с нужным `Chat`.

`before_send` применяется перед передачей прикладного RPC в транспорт.
Для отправки файла его предварительная загрузка может завершиться раньше
этого хука. Изменённый текст синхронизируется с локальным исходящим сообщением.

Для `after_rpc` `response` — TL-байты, `error` — словарь `code`, `name`,
`description`. Установлено ровно одно из этих полей. Восстанавливая ошибку,
поставь `error=None` и задай корректный ответ для типа исходного запроса.
Временные ошибки (`FLOOD_WAIT_*`, код 500 и выше), которые клиент повторяет
сам, в хук не попадают: он видит окончательный результат. Ошибка, которую
задал хук, получает код 400, если указан код вне 0–499, чтобы клиент не
повторял запрос.

Сообщения и ответы декодируются только для хуков, которые их обрабатывают:
хук с `request="messages.getHistory"` не замедляет остальные запросы. Хук без
фильтра видит все запросы, но байты ответа декодирует сам, через
`tl.decode`, если они ему нужны.

`HookResult()` и `None` означают `DEFAULT`. `MODIFY` применяет переданное
значение после проверки. `MODIFY_FINAL` завершает текущую цепочку после
применения. `CANCEL` прерывает операцию с объяснением из `reason`.
Обработчики выполняются по убыванию приоритета, затем по ID плагина.
При равном ID сохраняется порядок регистрации.

Каждому обработчику передаётся отдельная копия. Изменения без `MODIFY`
отбрасываются. Исключение или некорректный результат в `before_send` и
`before_rpc` прерывает отправку с уведомлением. В `after_rpc` и
`before_updates` ошибка хука показывается уведомлением, а клиент получает
исходный ответ или пакет обновлений: сломанный хук не ломает Telegram.
Пропустить пакет или превратить ответ в ошибку можно только явно, через
`CANCEL`. Хуки синхронные и выполняются на главном потоке.
Ожидаемые запросы следует создавать через `run_async`; связанная цепочка
передаёт список вызывавших её плагинов и пропускает их собственные хуки.

Пропуск входящего `Updates` сохраняет прежнее состояние последовательности
клиента. Следующие обновления могут потребовать догрузки различий Telegram.
`before_updates` перехватывает пакеты типа `Updates`; ответы догрузки
`updates.Difference` и `updates.ChannelDifference` доступны через `after_rpc`.
Протокольные сообщения и транспортные повторы обходят прикладной RPC-хук.

Возвращаемый `Registration` имеет `cancel()`. Отключение плагина удаляет все
его подписки и хуки, отменяет управляемые задачи и ожидающие операции SDK.

## Фоновые задачи и интерфейс

`self.run_async(coroutine)` и `desktop_utils.create_task` возвращают управляемый
`concurrent.futures.Future`. Его `cancel()` запрашивает отмену. Цикл `asyncio`
работает в отдельном потоке. `desktop_utils.run_in_background` выполняет
блокирующую функцию в пуле, `set_timer` создаёт одноразовый или повторный таймер.

```python
from desktop_utils import run_on_ui

async def background(self):
    rows = await client.accounts()
    await run_on_ui(lambda: self.set_setting("account_count", len(rows)))
```

`run_on_ui` принимает синхронную функцию и сохраняет её Python-результат.
Запись настроек выполняется на главном потоке. `get_account_setting` и
`set_account_setting` хранят значения раздельно по аккаунтам и сохраняют их
при обновлении и откате плагина. `file_utils.get_plugin_data_dir(account_id)`
возвращает отдельный каталог данных аккаунта. Настройки и каталоги данных
принадлежат экземпляру плагина (`installation_id`): два установленных
экземпляра с одним `__id__` их не делят.

Для кода внутри одного процесса отмена является кооперативной. Плагин с
бесконечным циклом или зависшей нативной библиотекой может потребовать перезапуска.

## Файлы

`desktop.media.send_file` загружает файл частями и отправляет его как документ.
Поддержаны подпись, тихая отправка, `InputFile` и `InputFileBig`.
`download_file` скачивает `Attachment` во временный файл и публикует результат
после проверки размера. Ошибка или отмена оставляет прежний файл назначения.
Ссылку вложения с истёкшим `file_reference` функция обновляет через сообщение.

Обе функции принимают `progress`, получающий `Progress` с ID аккаунта,
переданными байтами и общим размером. Возвращаемая coroutine отменяется
обычными средствами `asyncio`. Пример загружает файл по команде в Избранном
и скачивает вложение с подписью `/plugin-download` в каталог данных плагина.

## Примеры и проверка

- [Обработка текста и отмена](../tools/ovygram/examples/text_hooks.ovyplugin).
- [Перехват запроса истории и ответа](../tools/ovygram/examples/rpc_hooks.ovyplugin).
- [Аккаунты и события](../tools/ovygram/examples/account_events.ovyplugin).
- [Файлы и прогресс в Избранном](../tools/ovygram/examples/media_transfer.ovyplugin).

После будущей сборки проверяются несколько аккаунтов, фоновый аккаунт при
переключении окна, выход во время запроса, отмена передачи, сбой сети,
редактирование и удаление сообщений, конфликты хуков и повторное включение.
Эти проверки готового клиента дополняют локальные тесты Python и проверку исходников.

### Кнопки и подразделы настроек

`create_settings()` поддерживает `Header(text)` и
`Button(key, text, on_click)` из `ui.settings`, помимо `Switch`, `Input` и
`Selector`. Заголовок не хранит значение; кнопка вызывает обработчик,
принадлежащий текущему экземпляру плагина. Обработчик может быть `async def`.

```python
from ui.settings import Header, Button, Input

def create_settings(self):
    return [
        Header("Подключение"),
        Input("address", "Адрес", ""),
        Button("test", "Проверить подключение", self.test_connection),
    ]
```

В «Сохранить настройки» передаются только значения редактируемых полей.
Нажатие не принимает Python-код из интерфейса: используется идентификатор
действия текущего экземпляра. Старое действие после выключения, обновления
или выгрузки плагина не выполняется.

В `desktop.ui.add_menu_item` также поддерживается `menu="profile"` — меню
профиля пользователя, группы или канала. Обработчик получает аккаунт и
объект профиля в `MenuContext.chat`; `MenuContext.message` отсутствует.
Пункты `profile` и `chat` регистрируются раздельно.
