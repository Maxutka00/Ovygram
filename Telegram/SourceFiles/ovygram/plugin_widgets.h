#pragma once

#include <QtCore/QJsonObject>
#include <QtCore/QJsonValue>

#include <functional>

class QWidget;

namespace Ovygram::Widgets {

// Generic access to any Telegram widget through Qt, without upstream
// changes: widget tree, handles, selector rules, keys and properties.

void SetEventSender(std::function<void(QJsonObject)> send);

// Fire-and-forget "ui.widgets.*" and "ui.keys.*" commands.
void Handle(const QJsonObject &command);

// Requests with a reply: "widgets.tree" and "widgets.get".
[[nodiscard]] QJsonValue Request(const QJsonObject &command);

void RemovePlugin(const QString &pluginId);

// The widget behind a handle from widgets.tree, or nullptr if it is gone.
[[nodiscard]] QWidget *Resolve(const QJsonValue &handle);

} // namespace Ovygram::Widgets
