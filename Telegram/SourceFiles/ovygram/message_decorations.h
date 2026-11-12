#pragma once

#include <QtCore/QJsonObject>
#include <QtCore/QRect>

class HistoryItem;
class QPainter;

namespace Ovygram {

// Called when HistoryView::Message::draw() finishes. Paints plugin
// decorations of this message over its bubble.
void PaintMessage(QPainter &p, not_null<HistoryItem*> item, QRect bubble);

namespace MessageDecorations {

// "ui.message_decoration.set" and "ui.message_decoration.remove" commands.
void Handle(const QJsonObject &command);
void RemovePlugin(const QString &installationId);

} // namespace MessageDecorations
} // namespace Ovygram
