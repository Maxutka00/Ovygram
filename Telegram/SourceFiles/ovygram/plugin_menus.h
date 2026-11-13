#pragma once

#include <QtCore/QJsonObject>

#include <functional>

class PeerData;
class HistoryItem;

namespace Main {
class Session;
} // namespace Main

namespace Ui {
class PopupMenu;
class VerticalLayout;
namespace Menu {
struct MenuCallback;
} // namespace Menu
} // namespace Ui

namespace Window {
class SessionController;
} // namespace Window

namespace Ovygram {

// Called by Telegram menus (the only upstream-facing part). Each adds the
// items plugins registered for that menu, after Telegram's own items.

// The side menu with Settings, Night mode and so on.
void FillMainMenu(
	not_null<Ui::VerticalLayout*> menu,
	not_null<Window::SessionController*> controller);

// The chat menu: "⋮" in the chat top bar and the chat list context menu.
void FillChatMenu(PeerData *peer, const Ui::Menu::MenuCallback &addAction);

// The profile's own menu, distinct from the chat menu.
void FillProfileMenu(PeerData *peer, const Ui::Menu::MenuCallback &addAction);

// The message context menu in a chat.
void FillMessageMenu(not_null<Ui::PopupMenu*> menu, HistoryItem *item);

// Called by PluginUi.
namespace Menus {

// Describes a chat and a message as desktop.client does.
using Describer = std::function<QJsonObject(
	Main::Session &session,
	PeerData *peer,
	HistoryItem *item)>;

void SetEventSender(std::function<void(QJsonObject)> send);
void SetDescriber(Describer describer);

// Shared by native menu and panel actions; describes the actual clicked
// account/peer, independently of the account currently focused elsewhere.
[[nodiscard]] QJsonObject DescribeContext(Main::Session &session, PeerData *peer, HistoryItem *item);

// "ui.menu.add" and "ui.menu.remove".
void Handle(const QJsonObject &command);
void RemovePlugin(const QString &installationId);

} // namespace Menus
} // namespace Ovygram
