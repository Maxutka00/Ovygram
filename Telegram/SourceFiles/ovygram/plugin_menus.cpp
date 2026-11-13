#include "ovygram/plugin_menus.h"

#include "base/weak_ptr.h"
#include "data/data_peer.h"
#include "data/data_session.h"
#include "history/history.h"
#include "history/history_item.h"
#include "main/main_session.h"
#include "settings/settings_common.h"
#include "ui/widgets/buttons.h"
#include "ui/widgets/menu/menu_add_action_callback.h"
#include "ui/widgets/popup_menu.h"
#include "ui/wrap/vertical_layout.h"
#include "window/window_controller.h"
#include "window/window_session_controller.h"
#include "styles/style_menu_icons.h"
#include "styles/style_window.h"

#include <QtCore/QJsonArray>

#include <map>
#include <set>
#include <stdexcept>
#include <vector>

namespace Ovygram {
namespace {

constexpr auto kMaximumText = 64;
constexpr auto kMaximumItems = 64;

enum class Location {
	Main,
	Chat,
	Profile,
	Message,
};

struct Item {
	QString installationId;
	Location location = Location::Main;
	QString text;
	std::set<QString> kinds; // Chat kinds, empty for all.
};

struct State {
	std::map<QString, Item> items; // Rule ID -> item, ordered by ID.
	std::vector<QString> order; // Rule IDs in the order of adding.
	std::function<void(QJsonObject)> send;
	Menus::Describer describe;
};

State &Get() {
	static auto result = State();
	return result;
}

[[nodiscard]] QString ChatKind(not_null<PeerData*> peer) {
	return peerIsChannel(peer->id)
		? u"channel"_q
		: peerIsChat(peer->id)
		? u"chat"_q
		: u"user"_q;
}

// Items of the location, in the order plugins added them.
[[nodiscard]] std::vector<std::pair<QString, Item>> ItemsFor(
		Location location,
		PeerData *peer) {
	auto result = std::vector<std::pair<QString, Item>>();
	const auto &state = Get();
	for (const auto &id : state.order) {
		const auto i = state.items.find(id);
		if (i == end(state.items) || i->second.location != location) {
			continue;
		} else if (!i->second.kinds.empty()
			&& (!peer || !i->second.kinds.contains(ChatKind(peer)))) {
			continue;
		}
		result.emplace_back(*i);
	}
	return result;
}

void Clicked(
		const QString &ruleId,
		Main::Session *session,
		PeerData *peer,
		HistoryItem *item) {
	const auto &state = Get();
	const auto i = state.items.find(ruleId);
	if (i == end(state.items) || !state.send) {
		return;
	}
	auto value = (session && state.describe)
		? state.describe(*session, peer, item)
		: QJsonObject();
	if (session) {
		value.insert(u"account_id"_q, QString::number(session->uniqueId()));
	}
	state.send(QJsonObject{
		{ u"installation_id"_q, i->second.installationId },
		{ u"type"_q, u"menu_click"_q },
		{ u"rule_id"_q, ruleId },
		{ u"value"_q, value },
	});
}

[[nodiscard]] Location ParseLocation(const QString &value) {
	if (value == u"main"_q) {
		return Location::Main;
	} else if (value == u"chat"_q) {
		return Location::Chat;
	} else if (value == u"message"_q) {
		return Location::Message;
	} else if (value == u"profile"_q) {
		return Location::Profile;
	}
	throw std::runtime_error("Menu must be main, chat, profile or message.");
}

} // namespace

void FillMainMenu(
		not_null<Ui::VerticalLayout*> menu,
		not_null<Window::SessionController*> controller) {
	const auto weak = base::make_weak(controller);
	for (const auto &[id, item] : ItemsFor(Location::Main, nullptr)) {
		const auto ruleId = id;
		Settings::AddButtonWithIcon(
			menu,
			rpl::single(item.text),
			st::mainMenuButton,
			{ &st::menuIconCustomize }
		)->setClickedCallback([=] {
			if (const auto strong = weak.get()) {
				const auto session = &strong->session();
				// Closes the side menu, as Telegram's own items do.
				strong->window().hideSettingsAndLayer();
				Clicked(ruleId, session, nullptr, nullptr);
			}
		});
	}
}

void FillPeerMenu(Location location, PeerData *peer, const Ui::Menu::MenuCallback &addAction) {
	if (!peer) {
		return;
	}
	const auto session = base::make_weak(&peer->session());
	const auto peerId = peer->id;
	for (const auto &[id, item] : ItemsFor(location, peer)) {
		const auto ruleId = id;
		addAction(item.text, [=] {
			if (const auto strong = session.get()) {
				Clicked(
					ruleId,
					strong,
					strong->data().peerLoaded(peerId),
					nullptr);
			}
		}, &st::menuIconCustomize);
	}
}

void FillChatMenu(PeerData *peer, const Ui::Menu::MenuCallback &addAction) {
	FillPeerMenu(Location::Chat, peer, addAction);
}

void FillProfileMenu(PeerData *peer, const Ui::Menu::MenuCallback &addAction) {
	FillPeerMenu(Location::Profile, peer, addAction);
}

void FillMessageMenu(not_null<Ui::PopupMenu*> menu, HistoryItem *item) {
	if (!item) {
		return;
	}
	const auto items = ItemsFor(Location::Message, item->history()->peer);
	if (items.empty()) {
		return;
	}
	const auto session = base::make_weak(&item->history()->session());
	const auto itemId = item->fullId();
	if (!menu->empty()) {
		menu->addSeparator();
	}
	for (const auto &[id, entry] : items) {
		const auto ruleId = id;
		menu->addAction(entry.text, [=] {
			if (const auto strong = session.get()) {
				if (const auto found = strong->data().message(itemId)) {
					Clicked(
						ruleId,
						strong,
						found->history()->peer,
						found);
				}
			}
		}, &st::menuIconCustomize);
	}
}

namespace Menus {

void SetEventSender(std::function<void(QJsonObject)> send) {
	Get().send = std::move(send);
}

void SetDescriber(Describer describer) {
	Get().describe = std::move(describer);
}

QJsonObject DescribeContext(Main::Session &session, PeerData *peer, HistoryItem *item) {
	auto result = Get().describe ? Get().describe(session, peer, item) : QJsonObject();
	result.insert(u"account_id"_q, QString::number(session.uniqueId()));
	return result;
}

void Handle(const QJsonObject &command) {
	const auto method = command.value(u"method"_q).toString();
	const auto ruleId = command.value(u"rule_id"_q).toString();
	if (ruleId.isEmpty()) {
		throw std::runtime_error("A menu item needs an ID.");
	}
	auto &state = Get();
	if (method == u"ui.menu.add"_q) {
		auto item = Item{
			.installationId = command.value(u"installation_id"_q).toString(),
			.location = ParseLocation(command.value(u"menu"_q).toString()),
			.text = command.value(u"text"_q).toString().trimmed(),
		};
		if (item.text.isEmpty() || item.text.size() > kMaximumText) {
			throw std::runtime_error("Menu item text must have 1 to 64 characters.");
		}
		for (const auto &kind : command.value(u"kinds"_q).toArray()) {
			const auto value = kind.toString();
			if (value != u"user"_q && value != u"chat"_q && value != u"channel"_q) {
				throw std::runtime_error("Chat kinds are user, chat and channel.");
			}
			item.kinds.insert(value);
		}
		if (!state.items.contains(ruleId)) {
			if (state.items.size() >= kMaximumItems) {
				throw std::runtime_error("Too many plugin menu items.");
			}
			state.order.push_back(ruleId);
		}
		state.items[ruleId] = std::move(item);
	} else if (method == u"ui.menu.remove"_q) {
		state.items.erase(ruleId);
		std::erase(state.order, ruleId);
	} else {
		throw std::runtime_error("Unknown menu command.");
	}
}

void RemovePlugin(const QString &installationId) {
	auto &state = Get();
	std::erase_if(state.items, [&](const auto &entry) {
		return entry.second.installationId == installationId;
	});
	std::erase_if(state.order, [&](const QString &id) {
		return !state.items.contains(id);
	});
}

} // namespace Menus
} // namespace Ovygram
