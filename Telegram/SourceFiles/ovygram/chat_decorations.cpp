#include "ovygram/chat_decorations.h"

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

constexpr auto kMaximumOps = 64;

// A draw command, parsed once. Negative x / y count from the right / bottom
// edge of the row, because a plugin doesn't know the row size in advance.
struct Op {
	enum class Type { Rect, Ellipse, Line, Text };
	Type type = Type::Rect;
	double x = 0, y = 0, width = 0, height = 0;
	double x2 = 0, y2 = 0;
	double radius = 0;
	double lineWidth = 1;
	int size = 13;
	QColor color;
	QString text;
};

struct Decoration {
	QString pluginId;
	QString accountId;
	QString chatId; // "*" decorates every chat of the account.
	QColor background;
	std::vector<Op> ops;
};

struct State {
	std::map<QString, Decoration> decorations; // Decoration ID -> decoration.
};

State &Get() {
	static auto result = State();
	return result;
}

[[nodiscard]] QColor ParseColor(const QJsonValue &value) {
	const auto result = QColor(value.toString());
	if (!result.isValid()) {
		throw std::runtime_error("Invalid color, use #rrggbb or #aarrggbb.");
	}
	return result;
}

[[nodiscard]] std::vector<Op> ParseOps(const QJsonArray &commands) {
	if (commands.size() > kMaximumOps) {
		throw std::runtime_error("Too many draw commands in a decoration.");
	}
	auto result = std::vector<Op>();
	for (const auto &value : commands) {
		const auto command = value.toObject();
		const auto name = command.value(u"op"_q).toString();
		const auto number = [&](const char *key, double fallback = 0.) {
			return command.value(QLatin1String(key)).toDouble(fallback);
		};
		auto op = Op{
			.x = number("x"),
			.y = number("y"),
			.width = number("width"),
			.height = number("height"),
			.x2 = number("x2"),
			.y2 = number("y2"),
			.radius = number("radius"),
			.lineWidth = std::max(number("width", 1.), 1.),
			.size = std::clamp(int(number("size", 13.)), 6, 96),
			.color = ParseColor(command.value(u"color"_q)),
			.text = command.value(u"text"_q).toString(),
		};
		if (name == u"rect"_q) {
			op.type = Op::Type::Rect;
		} else if (name == u"ellipse"_q) {
			op.type = Op::Type::Ellipse;
		} else if (name == u"line"_q) {
			op.type = Op::Type::Line;
			op.x = number("x1");
			op.y = number("y1");
		} else if (name == u"text"_q) {
			op.type = Op::Type::Text;
		} else {
			throw std::runtime_error("Unknown draw command.");
		}
		result.push_back(std::move(op));
	}
	return result;
}

[[nodiscard]] double Resolve(double value, int size) {
	return (value < 0) ? (size + value) : value;
}

void Paint(QPainter &p, const std::vector<Op> &ops, QRect row) {
	for (const auto &op : ops) {
		const auto x = row.x() + Resolve(op.x, row.width());
		const auto y = row.y() + Resolve(op.y, row.height());
		switch (op.type) {
		case Op::Type::Rect:
			p.setPen(Qt::NoPen);
			p.setBrush(op.color);
			p.drawRoundedRect(
				QRectF(x, y, op.width, op.height),
				op.radius,
				op.radius);
			break;
		case Op::Type::Ellipse:
			p.setPen(Qt::NoPen);
			p.setBrush(op.color);
			p.drawEllipse(QRectF(x, y, op.width, op.height));
			break;
		case Op::Type::Line:
			p.setPen(QPen(op.color, op.lineWidth));
			p.drawLine(QPointF(x, y), QPointF(
				row.x() + Resolve(op.x2, row.width()),
				row.y() + Resolve(op.y2, row.height())));
			break;
		case Op::Type::Text: {
			auto font = p.font();
			font.setPixelSize(op.size);
			p.setFont(font);
			p.setPen(op.color);
			p.drawText(QPointF(x, y), op.text);
		} break;
		}
	}
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
		Paint(p, decoration.ops, row);
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
			.ops = ParseOps(command.value(u"commands"_q).toArray()),
		};
		if (decoration.accountId.isEmpty() || decoration.chatId.isEmpty()) {
			throw std::runtime_error("A decoration needs account_id and chat_id.");
		}
		const auto background = command.value(u"background"_q);
		if (!background.isNull() && !background.isUndefined()) {
			decoration.background = ParseColor(background);
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
