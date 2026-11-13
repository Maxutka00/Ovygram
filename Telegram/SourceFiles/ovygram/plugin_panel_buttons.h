#pragma once

#include <QtCore/QJsonObject>
#include <QtCore/QString>
#include <functional>

class QWidget;
class PeerData;

namespace Ovygram::PanelButtons {

// Only application code registers hosts. Plugins choose a documented panel,
// never an arbitrary parent widget. All functions run on the Qt main thread.
void RegisterHost(QWidget *owner, const QString &panel, std::function<void()> relayout);
void SetEventSender(std::function<void(QJsonObject)> send);
void Handle(const QJsonObject &command);
void RemovePlugin(const QString &installationId);

// Prepare selects buttons that fit and returns the space to reserve in the
// native layout. A null peer hides them (search, selection, recording, etc.).
[[nodiscard]] int Prepare(QWidget *owner, PeerData *peer, int availableWidth, int rowHeight);
void Place(QWidget *owner, int left, int top, int rowHeight);
void Hide(QWidget *owner);

} // namespace Ovygram::PanelButtons
