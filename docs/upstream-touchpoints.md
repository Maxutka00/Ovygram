# Upstream touchpoints

Ovygram code lives in its own files (`Telegram/SourceFiles/ovygram/`, the
`api_plugins`, `plugin_runtime` and `settings_plugins` files, and
`Telegram/cmake/ovygram.cmake`). Upstream files are changed only where there
is no other way, and each change is guarded by `#ifdef OVYGRAM_ENABLED`.

When updating the Telegram base, check every entry below. "Commits per year"
is the number of upstream commits that touched the file in the year before
November 2026; the higher it is, the more likely a merge conflict.

| File | Insertions | Commits per year | Purpose |
|---|---|---|---|
| `Telegram/CMakeLists.txt` | `include(cmake/ovygram.cmake)`, `output_name` for Windows and Linux | 416 | Build integration, binary name `Ovygram` |
| `Telegram/SourceFiles/history/view/history_view_chat_section.cpp` | include and one term in `top` in `ChatWidget::updateControlsGeometry()` | 156 | Plugin bars above the messages (`ui.ChatBar`) |
| `Telegram/SourceFiles/history/view/history_view_top_bar_widget.cpp` | include, `RegisterElements` in the constructor, `ApplyElementRules` before `updateControlsGeometry()` in `updateControlsVisibility()` | 46 | Named elements `chat.top_bar.*` (`ui.element`) |
| `Telegram/SourceFiles/dialogs/ui/dialogs_layout.cpp` | include and `PaintChatRow()` after `PaintRow()` in the chat row `RowPainter::Paint()` | 22 | Chat list decorations (`ui.decorate_chat`) |
| `Telegram/SourceFiles/history/view/controls/history_view_compose_controls.cpp` | include, `RegisterElements` in `init()`, `ApplyElementRules(_wrap.get())` at the end of `updateControlsVisibility()` | 171 | Named elements `compose.*` and the message field API |
| `Telegram/SourceFiles/dialogs/dialogs_entry.cpp` | include, a check at the start of `Entry::setChatListExistence()`, and `keepPinned` in `Entry::removeFromChatList()` | 9 | Chats hidden by plugins (`ui.hide_chats`) |
| `Telegram/SourceFiles/history/view/history_view_message.cpp` | include and a `gsl::finally` guard after the `isHidden()` return in `Message::draw()` | 150 | Message decorations (`ui.decorate_message`) |
| `Telegram/SourceFiles/window/window_main_menu.cpp` | include and `FillMainMenu()` at the end of `MainMenu::setupMenu()` | 25 | Plugin items in the side menu (`ui.add_menu_item("main")`) |
| `Telegram/SourceFiles/window/window_peer_menu.cpp` | include and `FillChatMenu()` after `Filler::fill()` in `FillDialogsEntryMenu()` | 82 | Plugin items in the chat menu (`"chat"`) |
| `Telegram/SourceFiles/history/view/history_view_context_menu.cpp` | include and `FillMessageMenu()` after `FillContextMenuItems()` in `FillContextMenu()` | 83 | Plugin items in the message menu (`"message"`) |
| `Telegram/SourceFiles/api/api_updates.cpp` | 7 | not measured | Update hooks and message events |
| `Telegram/SourceFiles/apiwrap.cpp` | 3 | not measured | Sent message events, sends cancelled by plugins (`sendMessage()` and `sendMessageFail()`) |
| `Telegram/SourceFiles/mtproto/mtp_instance.cpp` | 2 | not measured | RPC hooks; a request rejected by a plugin keeps its handlers in `_parserMap` |
| `Telegram/SourceFiles/core/application.{h,cpp}` | 2 and 3 | 59 (`.cpp`) | Plugin runtime lifetime |
| `Telegram/SourceFiles/core/launcher.{h,cpp}` | 2 and 2 | not measured | `--disable-plugins` |
| `Telegram/SourceFiles/settings/sections/settings_main.cpp` | 2 | 41 | Settings → Plugins entry |
| `Telegram/SourceFiles/window/window_session_controller.cpp` | 2 | not measured | `chat_changed` event |

## Chat bars

Chats are shown by `HistoryView::ChatWidget`; the older `HistoryWidget` still
exists but stays hidden without a chat, so it has no insertion.
`ChatWidget::updateControlsGeometry()` stacks Telegram's own bars in
`_topControls` and starts the messages at `top`. Ovygram adds the height
returned by `Ovygram::LayoutChatBars()`, which places plugin bars right below
`_topControls`, inside the chat widget. If upstream renames `top`,
`topControlsTop` or `_topControls`, move the call so that it receives the
bottom of the last Telegram bar. Plugin bars relayout the chat by sending it a
resize event, so no other upstream change is needed.

## Named elements

`Ovygram::RegisterElements()` gives built-in widgets stable names
(`chat.top_bar.call`, `chat.top_bar.search`, `chat.top_bar.info`,
`chat.top_bar.menu`, and `compose.attach`, `compose.emoji`, `compose.send`,
`compose.field` in `ComposeControls`). `ComposeControls::updateControlsGeometry()`
reserves the width of `_attachToggle` even when it is hidden, so hiding the
attach button leaves a gap. `Ovygram::ApplyElementRules()` must run after the owner
sets the visibility of these widgets and before it lays them out, so a hidden
button leaves no gap. If upstream renames `_call`, `_search`, `_infoToggle` or
`_menuToggle`, or moves the final `updateControlsGeometry()` call, update the
registration and the call. A widget shown outside that pass is hidden again by
an event filter, so a missed call only causes a short flicker.

## Chat list decorations

`Ovygram::PaintChatRow()` runs right after `PaintRow()` in the
`RowPainter::Paint()` overload for chat rows and paints plugin decorations
over the finished row. If upstream renames `peer`, `context.width` or
`context.active` there, update the call.

## Hidden chats

`Ovygram::HiddenFromChatList()` turns `exists` off in
`Dialogs::Entry::setChatListExistence()`, the single place that adds a chat
to the chat list and its folders. When a rule changes, Ovygram calls
`History::updateChatListExistence()` for the affected chats. Search uses other
paths and still finds hidden chats.

`Entry::removeFromChatList()` normally unpins a removed chat. A hidden chat
keeps its pin: it is still pinned on the server, and a pinned order saved
while it is hidden must keep listing it, or the server unpins it.

## Message decorations

`Message::draw()` has many returns, so the call is a `gsl::finally` guard
created right after the `isHidden()` return; it paints over the finished
message in bubble coordinates (`g`) on every later exit. By then the function
has undone the swipe-to-reply (`gestureShift`) and selection mode
(`selectionTranslation`) shifts, so the guard applies them again. If upstream
renames `g`, `gestureShift` or `selectionTranslation`, update the guard.

## Menus

Each menu gets plugin items after Telegram's own ones from one call:
`Ovygram::FillMainMenu()` at the end of `MainMenu::setupMenu()`,
`Ovygram::FillChatMenu()` in `FillDialogsEntryMenu()` (used by the "⋮" menu
of the chat top bar and the chat list context menu) and
`Ovygram::FillMessageMenu()` after `FillContextMenuItems()` in the message
`FillContextMenu()`. Menus are built each time they open, so the calls need
no notification when plugins change their items. If upstream splits these
functions, keep each call after the last item is added.
