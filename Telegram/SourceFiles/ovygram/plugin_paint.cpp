#include "ovygram/plugin_paint.h"

#include <QtGui/QPainter>

#include <stdexcept>

namespace Ovygram {
namespace {

double Resolve(double value, int size) {
	return (value < 0) ? (size + value) : value;
}

} // namespace

QColor ParsePaintColor(const QJsonValue &value) {
	const auto result = QColor(value.toString());
	if (!result.isValid()) {
		throw std::runtime_error("Invalid color, use #rrggbb or #aarrggbb.");
	}
	return result;
}

std::vector<PaintOp> ParsePaintOps(const QJsonArray &commands, int limit) {
	if (commands.size() > limit) {
		throw std::runtime_error("Too many draw commands.");
	}
	auto result = std::vector<PaintOp>();
	for (const auto &value : commands) {
		const auto command = value.toObject();
		const auto name = command.value(u"op"_q).toString();
		const auto number = [&](const char *key, double fallback = 0.) {
			return command.value(QLatin1String(key)).toDouble(fallback);
		};
		auto op = PaintOp{
			.x = number("x"),
			.y = number("y"),
			.width = number("width"),
			.height = number("height"),
			.x2 = number("x2"),
			.y2 = number("y2"),
			.radius = number("radius"),
			.lineWidth = std::max(number("width", 1.), 1.),
			.size = std::clamp(int(number("size", 13.)), 6, 96),
			.color = ParsePaintColor(command.value(u"color"_q)),
			.text = command.value(u"text"_q).toString(),
		};
		if (name == u"rect"_q) {
			op.type = PaintOp::Type::Rect;
		} else if (name == u"ellipse"_q) {
			op.type = PaintOp::Type::Ellipse;
		} else if (name == u"line"_q) {
			op.type = PaintOp::Type::Line;
			op.x = number("x1");
			op.y = number("y1");
		} else if (name == u"text"_q) {
			op.type = PaintOp::Type::Text;
		} else {
			throw std::runtime_error("Unknown draw command.");
		}
		result.push_back(std::move(op));
	}
	return result;
}

void PaintOps(QPainter &p, const std::vector<PaintOp> &ops, QRect row) {
	for (const auto &op : ops) {
		const auto x = row.x() + Resolve(op.x, row.width());
		const auto y = row.y() + Resolve(op.y, row.height());
		switch (op.type) {
		case PaintOp::Type::Rect:
			p.setPen(Qt::NoPen);
			p.setBrush(op.color);
			p.drawRoundedRect(
				QRectF(x, y, op.width, op.height),
				op.radius,
				op.radius);
			break;
		case PaintOp::Type::Ellipse:
			p.setPen(Qt::NoPen);
			p.setBrush(op.color);
			p.drawEllipse(QRectF(x, y, op.width, op.height));
			break;
		case PaintOp::Type::Line:
			p.setPen(QPen(op.color, op.lineWidth));
			p.drawLine(QPointF(x, y), QPointF(
				row.x() + Resolve(op.x2, row.width()),
				row.y() + Resolve(op.y2, row.height())));
			break;
		case PaintOp::Type::Text: {
			auto font = p.font();
			font.setPixelSize(op.size);
			p.setFont(font);
			p.setPen(op.color);
			p.drawText(QPointF(x, y), op.text);
		} break;
		}
	}
}

} // namespace Ovygram
