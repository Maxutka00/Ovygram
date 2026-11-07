# Перенос Android-плагинов

Плагины Ovygram написаны на Python и устроены как Android-плагины: класс
`BasePlugin`, метаданные в начале файла, `HookResult`, настройки через
`create_settings()`. Но Ovygram — Telegram Desktop, а не Android-клиент:
в нём нет Java, Android API и классов Android-клиента, поэтому плагин нужно
адаптировать. Эмуляции Android не будет.

Если включить Android-плагин без изменений, Ovygram покажет ошибку:
`__platform__` должен быть `"desktop"`, а импорт `android`, `java`, `jnius`,
`org` и подобных модулей сообщает, что плагин нужно перенести.

## Что остаётся как было

- Файл `.plugin` или `.py` с метаданными-литералами `__id__`, `__name__`,
  `__version__`, `__author__`, `__description__`.
- `from base_plugin import BasePlugin`, `on_plugin_load()`,
  `on_plugin_unload()`, `create_settings()`, `get_setting()`,
  `set_setting()`, `log()`.
- `HookResult` и `HookStrategy` со стратегиями `DEFAULT`, `MODIFY`,
  `MODIFY_FINAL`, `CANCEL`: их можно импортировать из `base_plugin`, как в
  Android-плагинах, или из `hook_utils`.

## Что поменять

**Метаданные.** Добавьте `__platform__ = "desktop"` и
`__desktop_sdk__ = 2`. Поля, которых в Ovygram нет (например, иконка или
минимальная версия Android-клиента), можно оставить — они не читаются.
Сторонние библиотеки перечисляются в `__requirements__`, см.
[зависимости](dependencies.md).

**Настройки.** Поддерживаются `Switch`, `Input` и `Selector` из
`ui.settings`. Заголовки, разделители и текстовые строки уберите.

**Доступ к Telegram.** Вместо объектов Android-клиента — асинхронный
`desktop.client` и типизированные TL-объекты `desktop.tl`:

| Задача | В Ovygram |
| --- | --- |
| Отправить сообщение | `await client.send_message(chat, text)` |
| Любой запрос Telegram API | `await client.rpc(account, tl.messages.getHistory(...))` |
| Аккаунты | `await client.accounts()`; у запросов аккаунт указывается явно |
| Открытый чат | `await client.current_chat(account)` |
| Файлы | `desktop.media.send_file`, `download_file` |

Имена TL-объектов — как в схеме Telegram: `tl.messages.sendMessage`,
`tl.inputPeerUser`, без префиксов `TL_` и `TLRPC`. Ответ приходит как
результат `await`, а не в колбэк.

**Хуки.**

| Android-плагин | Ovygram |
| --- | --- |
| Хук отправки сообщения | `self.add_hook("before_send", callback)`, аргумент `OutgoingMessage` |
| Хук перед запросом по имени TL-метода | `self.add_hook("before_rpc", callback, request="messages.sendMessage")` |
| Хук после ответа | `self.add_hook("after_rpc", callback, request=...)` |
| Хук обновлений | `self.add_hook("before_updates", callback)` или события `subscribe("new_message", ...)` |

Хуки синхронные и возвращают `HookResult`; изменённое значение передаётся
в `HookResult(MODIFY, value)`. Подробности — в [SDK](sdk.md#хуки).

**Меню и интерфейс.** Пункты меню добавляет
`ui.add_menu_item("message" | "chat" | "main", text, callback)`. Вместо
Android-диалогов и всплывающих уведомлений — `ui.show_dialog`, окна,
полосы в чате и страницы из [`desktop.ui`](ui.md). Отдельного API
всплывающих уведомлений пока нет.

**Потоки.** Обработчики интерфейса и синхронные хуки выполняются в главном
потоке. Долгую работу запускайте через `self.run_async(coroutine)`,
блокирующие вызовы — через `desktop_utils.run_in_background`, а вернуться в
главный поток помогает `await desktop_utils.run_on_ui(callback)`.

## Порядок переноса

1. Скопируйте плагин в [шаблон](../tools/ovygram/template) или оставьте одним
   файлом, поменяйте метаданные.
2. Уберите импорты Android, Java и классов Android-клиента; замените вызовы
   по таблицам выше.
3. Перепишите обращения к Telegram на `await client...` внутри
   `async def` и `self.run_async(...)`.
4. Импортируйте плагин, включите и смотрите ошибки на его карточке и в
   журнале (см. [отладку](guide.md#отладка)).
