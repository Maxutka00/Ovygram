#pragma once

#include <QtCore/QJsonObject>

namespace Dialogs {
class Entry;
} // namespace Dialogs

namespace Ovygram {

// Called from Dialogs::Entry::setChatListExistence(). A chat hidden by a
// plugin leaves the chat list and every folder the usual way.
[[nodiscard]] bool HiddenFromChatList(not_null<Dialogs::Entry*> entry);

namespace ChatListFilter {

// "ui.chat_list.hide" and "ui.chat_list.unhide" commands.
void Handle(const QJsonObject &command);
void RemovePlugin(const QString &pluginId);

} // namespace ChatListFilter
} // namespace Ovygram
