#include "ovygram/chat_decorations.h"

#include "ovygram/plugin_paint.h"

#include "data/data_peer.h"
#include "main/main_session.h"

#include <QtCore/QJsonArray>
#include <QtGui/QColor>
#include <QtGui/QPainter>
#include <QtWidgets/QApplication>
#include <QtWidgets/QWidget>

#include <cstdlib>
#include <map>
#include <typeinfo>
#include <stdexcept>
#include <vector>

#ifndef _MSC_VER
#include <cxxabi.h>
#endif // !_MSC_VER

namespace Ovygram {
namespace {

struct Decoration {
	QString pluginId;
	QString accountId;
	QString chatId; // "*" decorates every chat of the account.
	QColor background;
	std::vector<PaintOp> ops;
};

struct State {
	std::map<QString, Decoration> decorations; // Decoration ID -> decoration.
};

State &Get() {
	static auto result = State();
	return result;
}

[[nodiscard]] bool IsChatList(QWidget *widget) {
	const auto raw = typeid(*widget).name();
#ifdef _MSC_VER
	return QLatin1String(raw).endsWith(QLatin1String("Dialogs::InnerWidget"));
#else // _MSC_VER
	auto status = 0;
	const auto demangled = abi::__cxa_demangle(raw, nullptr, nullptr, &status);
	const auto result = (status == 0 && demangled)
		&& (QLatin1String(demangled) == QLatin1String("Dialogs::InnerWidget"));
	std::free(demangled);
	return result;
#endif // _MSC_VER
}

void RepaintChatLists() {
	for (const auto widget : QApplication::allWidgets()) {
		if (widget->isVisible() && IsChatList(widget)) {
			widget->update();
		}
	}
}

} // namespace

void PaintChatRow(QPainter &p, PeerData *peer, QRect row, bool active) {
	const auto &decorations = Get().decorations;
	if (!peer || decorations.empty()) {
		return;
	}
	const auto accountId = QString::number(peer->session().uniqueId());
	const auto chatId = QString::number(peer->id.value);
	p.save();
	p.setRenderHint(QPainter::Antialiasing);
	for (const auto &[id, decoration] : decorations) {
		if (decoration.accountId != accountId
			|| (decoration.chatId != chatId && decoration.chatId != u"*"_q)) {
			continue;
		}
		// The active row has its own strong background; keep it readable.
		if (decoration.background.isValid() && !active) {
			p.fillRect(row, decoration.background);
		}
		PaintOps(p, decoration.ops, row);
	}
	p.restore();
}

namespace Decorations {

void Handle(const QJsonObject &command) {
	const auto method = command.value(u"method"_q).toString();
	const auto id = command.value(u"decoration_id"_q).toString();
	if (id.isEmpty()) {
		throw std::runtime_error("A decoration needs an ID.");
	}
	auto &decorations = Get().decorations;
	if (method == u"ui.decoration.set"_q) {
		auto decoration = Decoration{
			.pluginId = command.value(u"plugin_id"_q).toString(),
			.accountId = command.value(u"account_id"_q).toString(),
			.chatId = command.value(u"chat_id"_q).toString(),
			.ops = ParsePaintOps(command.value(u"commands"_q).toArray()),
		};
		if (decoration.accountId.isEmpty() || decoration.chatId.isEmpty()) {
			throw std::runtime_error("A decoration needs account_id and chat_id.");
		}
		const auto background = command.value(u"background"_q);
		if (!background.isNull() && !background.isUndefined()) {
			decoration.background = ParsePaintColor(background);
		}
		decorations[id] = std::move(decoration);
	} else if (method == u"ui.decoration.remove"_q) {
		decorations.erase(id);
	} else {
		throw std::runtime_error("Unknown decoration command.");
	}
	RepaintChatLists();
}

void RemovePlugin(const QString &pluginId) {
	const auto removed = std::erase_if(Get().decorations, [&](const auto &entry) {
		return entry.second.pluginId == pluginId;
	});
	if (removed) {
		RepaintChatLists();
	}
}

} // namespace Decorations
} // namespace Ovygram
