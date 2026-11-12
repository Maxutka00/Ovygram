#pragma once

#include <QtCore/QJsonObject>
#include <QtCore/QJsonValue>

#include <functional>

namespace Ovygram::Native {

// desktop.native: top-level window events and Qt signals, slots and
// invokable methods of any widget, without upstream changes.

void SetEventSender(std::function<void(QJsonObject)> send);

// "ui.native.windows", "ui.native.connect" and "ui.native.disconnect".
void Handle(const QJsonObject &command);

// Requests with a reply: "native.methods" and "native.invoke".
[[nodiscard]] QJsonValue Request(const QJsonObject &command);

void RemovePlugin(const QString &installationId);

} // namespace Ovygram::Native
