#pragma once

#include <QtCore/QJsonObject>
#include <QtCore/QJsonValue>

#include <functional>

class QVariant;
class QWidget;

namespace Ovygram::Widgets {

// Generic access to any Telegram widget through Qt, without upstream
// changes: widget tree, handles, selector rules, keys and properties.

void SetEventSender(std::function<void(QJsonObject)> send);

// Fire-and-forget "ui.widgets.*" and "ui.keys.*" commands.
void Handle(const QJsonObject &command);

// Requests with a reply: "widgets.tree" and "widgets.get".
[[nodiscard]] QJsonValue Request(const QJsonObject &command);

void RemovePlugin(const QString &installationId);

// The widget behind a handle from widgets.tree, or nullptr if it is gone.
[[nodiscard]] QWidget *Resolve(const QJsonValue &handle);

// Shared with desktop.native.
[[nodiscard]] QString HandleFor(QWidget *widget);
[[nodiscard]] QString ClassNameOf(const QWidget *widget);
[[nodiscard]] QJsonValue VariantToJson(const QVariant &value);
// Throws std::runtime_error when the value can't become that type.
[[nodiscard]] QVariant JsonToVariant(const QJsonValue &value, int typeId);

} // namespace Ovygram::Widgets
