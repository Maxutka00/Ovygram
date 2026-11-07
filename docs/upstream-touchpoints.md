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
| `Telegram/SourceFiles/api/api_updates.cpp` | 7 | not measured | Update hooks and message events |
| `Telegram/SourceFiles/apiwrap.cpp` | 2 | not measured | Sent message events |
| `Telegram/SourceFiles/mtproto/mtp_instance.cpp` | 2 | not measured | RPC hooks |
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
`chat.top_bar.menu`). `Ovygram::ApplyElementRules()` must run after the owner
sets the visibility of these widgets and before it lays them out, so a hidden
button leaves no gap. If upstream renames `_call`, `_search`, `_infoToggle` or
`_menuToggle`, or moves the final `updateControlsGeometry()` call, update the
registration and the call. A widget shown outside that pass is hidden again by
an event filter, so a missed call only causes a short flicker.
