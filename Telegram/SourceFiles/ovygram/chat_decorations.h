#pragma once

#include <QtCore/QJsonObject>
#include <QtCore/QRect>

class PeerData;
class QPainter;

namespace Ovygram {

// Called from Dialogs::Ui::RowPainter::Paint() after a chat row is painted.
// Draws plugin decorations of this chat over the row.
void PaintChatRow(QPainter &p, PeerData *peer, QRect row, bool active);

namespace Decorations {

// "ui.decoration.set" and "ui.decoration.remove" commands.
void Handle(const QJsonObject &command);
void RemovePlugin(const QString &installationId);

} // namespace Decorations
} // namespace Ovygram
