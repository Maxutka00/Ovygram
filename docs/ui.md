# Интерфейс плагинов: `desktop.ui`

Модуль `desktop.ui` даёт плагину собственные окна и страницы, пункты меню и
доступ к интерфейсу Telegram. Нужен `__desktop_sdk__ = 2`.

Все функции можно вызывать из любого потока: из `on_plugin_load`, хука или
фоновой задачи. Вызов только ставит команду в очередь, клиент выполняет её в
главном потоке. Обработчики событий интерфейса всегда вызываются в главном
потоке; обработчик может быть coroutine-функцией, тогда он запускается как
управляемая задача плагина.

Всё, что плагин создал или изменил, принадлежит ему и снимается при
выгрузке: окна закрываются, правила и декорации удаляются, цвета и скрытые
элементы возвращаются.

## Элементы

Содержимое окна — дерево элементов.

| Элемент | Назначение |
| --- | --- |
| `Column(*children)` | Элементы друг под другом |
| `Row(*children, align="center", spacing=8)` | Элементы в строку; `align` — `top`, `center`, `bottom` |
| `Text(text, align="left")` | Текст; `align` — `left`, `center`, `right` |
| `Button(text, on_click=None)` | Кнопка, `on_click()` |
| `Input(text="", placeholder="", on_change=None)` | Поле ввода, `on_change(text)` |
| `Switch(text, value=False, on_toggle=None)` | Переключатель, `on_toggle(value)` |
| `Image(path, height=0)` | Картинка из файла |
| `Spacer(height)` | Отступ |
| `Canvas(height, commands=(), on_click=None)` | Собственная отрисовка, `on_click(x, y)` |

У любого элемента внутри `Row` есть `width` (пиксели или `"fit"` — по
содержимому) и `stretch` (доля свободного места, по умолчанию 1).

```python
ui.Row(
    ui.Spacer(0, stretch=1),
    ui.Text("По центру", width="fit"),
    ui.Spacer(0, stretch=1),
)
```

### Отрисовка

Команды для `Canvas`, декораций чатов и сообщений:

| Команда | Что рисует |
| --- | --- |
| `fill_rect(x, y, width, height, color, radius=0)` | Прямоугольник |
| `line(x1, y1, x2, y2, color, width=1)` | Линию |
| `ellipse(x, y, width, height, color)` | Эллипс |
| `text(x, y, value, color, size=13)` | Текст, `y` — базовая линия |

Цвет — `#rrggbb` или `#aarrggbb`. Отрицательные `x` и `y` отсчитываются от
правого и нижнего края: `fill_rect(-28, 8, 20, 20, ...)` — квадрат у правого
края. У холста до 2000 команд, у декорации до 64.

## Поверхности

| Класс | Где показывается |
| --- | --- |
| `Dialog(content, title="", width=0)`, `show_dialog(...)` | Окно поверх Telegram |
| `Window(content, title="", width=420, height=480)` | Отдельное окно, содержимое прокручивается |
| `Section(content, title="")` | Страница в основной колонке вместо чата |
| `ChatBar(chat, content)` | Полоса над сообщениями одного чата |
| `Overlay(widget, canvas)` | Холст поверх любого виджета Telegram |

У всех есть `on_close` и методы:

- `show()` — показать, возвращает саму поверхность;
- `update(node, **props)` — изменить `text` у `Text`, `Button`, `Input`,
  `value` у `Switch`, `commands` у `Canvas`;
- `draw(canvas, commands)` — перерисовать холст;
- `close()` — закрыть. После закрытия `update()` бросает `ObjectDestroyed`.

Изменения, сделанные через `update()`, не возвращаются в `on_change` и
`on_toggle`, поэтому обработчик может менять своё же поле без зацикливания.

```python
class CounterPlugin(BasePlugin):
    def on_plugin_load(self):
        self.count = 0
        self.label = ui.Text("Нажатий: 0")
        self.window = ui.Window(ui.Column(
            self.label,
            ui.Button("Нажать", on_click=self.on_click),
        ), title="Счётчик").show()

    def on_click(self):
        self.count += 1
        self.window.update(self.label, text=f"Нажатий: {self.count}")
```

**Section** открывается в активном окне и участвует в истории переходов:
пользователь может открыть чат и вернуться кнопкой «Назад». Раздел
закрывается вызовом `close()`, при выгрузке плагина или когда история окна
его отбрасывает (например, при переходе к чату из списка); тогда вызывается
`on_close`.

**ChatBar** виден, пока этот чат открыт в окне, и остаётся до `close()`,
даже если пользователь уходит в другие чаты.

**Overlay** следует за размером виджета. Без `on_click` у холста клики
проходят сквозь него.

## Меню

```python
ui.add_menu_item("message", "Скопировать текст",
                 lambda menu: ui.set_clipboard(menu.message.text))
```

`add_menu_item(menu, text, callback, kinds=None)` добавляет пункт после
пунктов Telegram:

| `menu` | Меню |
| --- | --- |
| `"main"` | Боковое главное меню |
| `"chat"` | «⋮» в верхней панели чата и контекстное меню чата в списке |
| `"profile"` | Меню профиля пользователя, группы или канала |
| `"message"` | Контекстное меню сообщения |

`callback(menu)` получает `MenuContext` с полями `account_id`, `chat`
(`Chat`) и `message` (`Message`); для главного меню `chat` и `message` —
`None`. `kinds` ограничивает пункты чатов и сообщений типами чатов: `user`,
`chat` (обычная группа), `channel` (каналы и супергруппы). Пункт появляется
при следующем открытии меню. Результат имеет `remove()`.

## Свои кнопки в панелях Telegram

`add_panel_button(panel, text, callback, *, tooltip="", width=40, priority=0,
enabled=True, visible=True, chat=None, kinds=None)` создаёт нативную кнопку:

| `panel` | Место |
| --- | --- |
| `"chat.top_bar"` | Верхняя панель открытого чата, перед штатными кнопками справа |
| `"compose"` | Строка ввода, после кнопок вложения/отправителя и перед текстовым полем |

```python
self.panel_button = ui.add_panel_button(
    "chat.top_bar", "★", self.on_panel_click, tooltip="Действие плагина")

def on_panel_click(self, panel):
    self.log(f"Нажатие: аккаунт {panel.account_id}, чат {panel.chat.id}")
    self.panel_button.update(text="✓", tooltip="Выполнено")
```

Обработчик получает `PanelContext(account_id, chat, panel)` с настоящим
аккаунтом и чатом окна, в котором нажали кнопку. Поддерживается `async def`.
Без фильтров кнопка доступна во всех подходящих открытых чатах; `chat=Chat`
ограничивает её конкретным чатом и аккаунтом, `kinds=["user", "chat", "channel"]`
— типами чатов. Это те же типы, что у пунктов меню.

Возвращается `PanelButton`: `update(text=..., tooltip=..., width=...,
priority=..., enabled=..., visible=...)`, `show()`, `hide()`, `remove()`.
При выгрузке экземпляра его кнопки и обработчики удаляются; после удаления
`update()` вызывает `ObjectDestroyed`.

`width` — желаемая ширина 32–160 логических пикселей; круглая кнопка не бывает
уже своей высоты. Выше `priority` — раньше получает место; при равенстве
сохраняется порядок добавления. Допустимый приоритет: −10000…10000.
Подпись — до 32 единиц UTF-16, подсказка — до 256. Лимиты: 16 кнопок
на экземпляр и 64 во всём клиенте.

Кнопки участвуют в штатной раскладке. Они занимают не более трети ширины
панели и скрываются при нехватке места, сохраняя место штатным элементам.
Верхняя панель скрывает их при поиске, выделении сообщений и переходах;
строка ввода — при записи, скрытом поле и режимах без дополнительных кнопок.
Внешний вид и эти переходы нужно проверить в собранном клиенте по
[чек-листу](ui-checklist.md).

## Элементы Telegram

Встроенные кнопки с постоянными именами (`ui.ELEMENTS`):

| Имя | Элемент |
| --- | --- |
| `chat.top_bar.call`, `.search`, `.info`, `.menu` | Кнопки верхней панели чата |
| `compose.attach`, `compose.emoji`, `compose.send`, `compose.field` | Строка ввода |

```python
ui.element("chat.top_bar.call").hide()
ui.element("chat.top_bar.search").on_click(self.on_search, replace=True)
```

`hide()` / `show()` — скрытая кнопка не оставляет пустого места (кроме
`compose.attach`, под которую Telegram резервирует ширину).
`on_click(callback, replace=False)` — обработчик нажатия; с `replace=True`
Telegram нажатие не получает. `off_click()` снимает обработчик.

## Любой виджет через Qt

- `await widget_tree(depth=8, root=None)` — дерево виджетов активного окна:
  `handle`, `cls` (класс C++), `visible`, `geometry`, а также `name`,
  `accessible`, `element` и `children`, если есть. Пример
  `widget_inspector` показывает его по Ctrl+Shift+I.
- `await get_property(widget, name)`, `set_property(widget, name, value)` —
  свойства Qt. Telegram может перезаписать значение при следующей раскладке.
- `hide_widgets(**selector)` — скрывает подходящие виджеты сейчас и при
  каждом показе; родитель не перераскладывается.
- `on_widget_click(callback, replace=False, **selector)` — нажатия.
- `on_key(sequence, callback, replace=False, element=None)` — сочетание
  вроде `"Ctrl+Alt+K"`; с `replace=True` выигрывает у сочетаний Telegram, с
  `element` работает только при фокусе в этом элементе.

Селектор: `cls`, `ancestor` (класс любого родителя), `name` (objectName),
`accessible` (зависит от языка интерфейса), `element`, `index` (номер среди
подходящих соседей). Нужен хотя бы один из `cls`, `name`, `accessible`,
`element`. Правило действует и на виджеты, созданные позже.

### Сигналы и слоты: `desktop.native`

Для того, чего нет в `desktop.ui`, — низкоуровневый доступ к Qt-объектам:

- `native.on_window(callback)` — `callback(event)` при показе и скрытии
  окон, диалогов и всплывающих меню; `event` — словарь с `event`
  (`shown`/`hidden`), `handle`, `cls`, `kind` (`window`, `dialog`, `popup`,
  `other`) и `title`;
- `native.connect(widget, signal, callback)` — `callback(*args)` при каждом
  сигнале, например `"windowTitleChanged"`; соединение живёт до `remove()`,
  уничтожения виджета или выгрузки;
- `await native.methods(widget)` — сигналы, слоты и методы виджета;
- `await native.invoke(widget, name, *args)` — вызов слота или
  invokable-метода, возвращает результат.

Имена здесь — внутренние имена Telegram и Qt, они меняются между версиями.
Вызов произвольных методов может сломать клиент, как и любой код плагина.
Пример `native_events` пишет в журнал открытие окон и меню.

## Строка ввода

| Функция | Что делает |
| --- | --- |
| `await compose_text()` | Текст поля или `None` |
| `await compose_state()` | `{text, cursor, selection_start, selection_end}` |
| `set_compose_text(text)` | Заменить текст |
| `insert_compose_text(text)` | Вставить у курсора |
| `replace_compose_text(start, end, text, select=False)` | Заменить диапазон, `select` выделяет вставку |
| `on_compose_change(callback)` | `callback(state)` при правке пользователем |

Позиции — индексы Python-строки `state["text"]`, эмодзи считается одним
символом. Правки, сделанные этими функциями, в `on_compose_change` не
приходят. Пример `math_autocomplete` подсказывает результат выражения.

## Список чатов и сообщения

- `decorate_chat(chat, commands=(), background=None, account=None)` —
  рисование поверх строки чата; `chat="*"` с `account` — все чаты аккаунта.
- `hide_chats([chat, ...])` — скрыть чаты из списка и папок. Поиск их
  находит, закрепление сохраняется.
- `decorate_message(message, commands=(), background=None)` — рисование
  поверх пузыря сообщения.

Всё рисуется поверх строки или пузыря, поэтому `background` должен быть
полупрозрачным (`#22ff9800`): непрозрачный цвет закрывает текст. У
декораций есть `update(commands, background)` и `remove()`.

## Прочее

- `set_colors({"windowBg": "#101820"})` / `reset_colors()` — цвета темы на
  лету; неизвестное имя отменяет весь вызов.
- `set_clipboard(text)` — буфер обмена.

## Примеры

| Пример | Что показывает |
| --- | --- |
| [`ui_widgets`](../tools/ovygram/examples/ui_widgets.ovyplugin) | Окно, холст, диалог |
| [`chat_bar`](../tools/ovygram/examples/chat_bar.ovyplugin) | Полоса в чате |
| [`section`](../tools/ovygram/examples/section.ovyplugin) | Страница плагина из главного меню |
| [`menus`](../tools/ovygram/examples/menus.ovyplugin) | Пункты в трёх меню |
| [`panel_buttons`](../tools/ovygram/examples/panel_buttons.ovyplugin) | Кнопки в верхней панели и строке ввода, контекст нажатия |
| [`top_bar`](../tools/ovygram/examples/top_bar.ovyplugin) | Скрытие и перехват кнопок, цвета |
| [`widget_inspector`](../tools/ovygram/examples/widget_inspector.ovyplugin) | Дерево виджетов, Ctrl+Shift+I |
| [`chat_style`](../tools/ovygram/examples/chat_style.ovyplugin) | Декорация чатов, Ctrl+Alt+U |
| [`highlight`](../tools/ovygram/examples/highlight.ovyplugin) | Декорация сообщений, скрытие чата, Ctrl+Alt+H |
| [`math_autocomplete`](../tools/ovygram/examples/math_autocomplete.ovyplugin) | Работа со строкой ввода |
| [`native_events`](../tools/ovygram/examples/native_events.ovyplugin) | События окон и сигналы Qt, Ctrl+Alt+N |

Все точки перехвата собраны в [справочнике](hooks.md). Проверка в клиенте —
по [чек-листу](ui-checklist.md).
