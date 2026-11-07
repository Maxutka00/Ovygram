#include "ovygram/message_decorations.h"

#include "ovygram/plugin_paint.h"

#include "core/application.h"
#include "data/data_peer.h"
#include "data/data_session.h"
#include "history/history.h"
#include "history/history_item.h"
#include "main/main_account.h"
#include "main/main_domain.h"
#include "main/main_session.h"

#include <QtGui/QPainter>

#include <map>
#include <stdexcept>
#include <vector>

namespace Ovygram {
namespace {

struct Decoration {
	QString pluginId;
	QString accountId;
	QString chatId;
	MsgId messageId = 0;
	QColor background;
	std::vector<PaintOp> ops;
};

std::map<QString, Decoration> &Decorations() {
	static auto result = std::map<QString, Decoration>();
	return result;
}

void Repaint(const Decoration &decoration) {
	for (const auto &entry : Core::App().domain().accounts()) {
		const auto session = entry.account->maybeSession();
		if (!session
			|| QString::number(session->uniqueId()) != decoration.accountId) {
			continue;
		}
		const auto item = session->data().message(
			PeerId(decoration.chatId.toULongLong()),
			decoration.messageId);
		if (item) {
			session->data().requestItemRepaint(item);
		}
	}
}

} // namespace

void PaintMessage(QPainter &p, not_null<HistoryItem*> item, QRect bubble) {
	const auto &decorations = Decorations();
	if (decorations.empty()) {
		return;
	}
	const auto accountId = QString::number(item->history()->session().uniqueId());
	const auto chatId = QString::number(item->history()->peer->id.value);
	auto painted = false;
	for (const auto &[id, decoration] : decorations) {
		if (decoration.messageId != item->id
			|| decoration.chatId != chatId
			|| decoration.accountId != accountId) {
			continue;
		}
		if (!painted) {
			p.save();
			p.setRenderHint(QPainter::Antialiasing);
			painted = true;
		}
		if (decoration.background.isValid()) {
			p.setPen(Qt::NoPen);
			p.setBrush(decoration.background);
			p.drawRoundedRect(bubble, 8, 8);
		}
		PaintOps(p, decoration.ops, bubble);
	}
	if (painted) {
		p.restore();
	}
}

namespace MessageDecorations {

void Handle(const QJsonObject &command) {
	const auto method = command.value(u"method"_q).toString();
	const auto id = command.value(u"decoration_id"_q).toString();
	if (id.isEmpty()) {
		throw std::runtime_error("A decoration needs an ID.");
	}
	auto &decorations = Decorations();
	if (method == u"ui.message_decoration.set"_q) {
		auto decoration = Decoration{
			.pluginId = command.value(u"plugin_id"_q).toString(),
			.accountId = command.value(u"account_id"_q).toString(),
			.chatId = command.value(u"chat_id"_q).toString(),
			.messageId = MsgId(command.value(u"message_id"_q).toInteger()),
			.ops = ParsePaintOps(command.value(u"commands"_q).toArray()),
		};
		if (decoration.accountId.isEmpty()
			|| decoration.chatId.isEmpty()
			|| !decoration.messageId) {
			throw std::runtime_error("A message decoration needs a message.");
		}
		const auto background = command.value(u"background"_q);
		if (!background.isNull() && !background.isUndefined()) {
			decoration.background = ParsePaintColor(background);
		}
		Repaint(decorations[id] = std::move(decoration));
	} else if (method == u"ui.message_decoration.remove"_q) {
		if (const auto i = decorations.find(id); i != end(decorations)) {
			const auto removed = std::move(i->second);
			decorations.erase(i);
			Repaint(removed);
		}
	} else {
		throw std::runtime_error("Unknown message decoration command.");
	}
}

void RemovePlugin(const QString &pluginId) {
	auto removed = std::vector<Decoration>();
	auto &decorations = Decorations();
	for (auto i = begin(decorations); i != end(decorations);) {
		if (i->second.pluginId == pluginId) {
			removed.push_back(std::move(i->second));
			i = decorations.erase(i);
		} else {
			++i;
		}
	}
	for (const auto &decoration : removed) {
		Repaint(decoration);
	}
}

} // namespace MessageDecorations
} // namespace Ovygram
