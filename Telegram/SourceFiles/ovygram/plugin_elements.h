#pragma once

#include <QtCore/QJsonObject>

#include <functional>
#include <initializer_list>
#include <utility>

class QWidget;

namespace Ovygram {

// Called by Telegram widgets (the only upstream-facing part).
//
// Gives built-in widgets stable names, so plugins can hide them or handle
// their clicks. A name can belong to several widgets, one per window.
void RegisterElements(
	std::initializer_list<std::pair<const char*, QWidget*>> elements);

// Called after the owner set the visibility of its children and before it
// lays them out, so hidden elements leave no gap.
void ApplyElementRules(QWidget *owner);

// Called by PluginUi.
namespace Elements {

void SetEventSender(std::function<void(QJsonObject)> send);
void Handle(const QJsonObject &command);
void RemovePlugin(const QString &pluginId);

} // namespace Elements
} // namespace Ovygram
