#pragma once

#include <QtCore/QJsonArray>
#include <QtCore/QJsonValue>
#include <QtCore/QRect>
#include <QtGui/QColor>

#include <vector>

class QPainter;

namespace Ovygram {

// A plugin draw command, parsed once. Negative x / y count from the right /
// bottom edge of the area, because a plugin doesn't know its size in advance.
struct PaintOp {
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

[[nodiscard]] QColor ParsePaintColor(const QJsonValue &value);
// Decorations repaint with Telegram rows, so they get fewer commands than
// a plugin's own canvas.
inline constexpr auto kMaximumDecorationOps = 64;
[[nodiscard]] std::vector<PaintOp> ParsePaintOps(
	const QJsonArray &commands,
	int limit = kMaximumDecorationOps);
void PaintOps(QPainter &p, const std::vector<PaintOp> &ops, QRect area);

} // namespace Ovygram
