#include "ovygram/plugin_widgets.h"

#include "ovygram/plugin_elements.h"

#include <QtCore/QJsonArray>
#include <QtCore/QMetaProperty>
#include <QtCore/QPointer>
#include <QtGui/QKeyEvent>
#include <QtGui/QKeySequence>
#include <QtGui/QMouseEvent>
#include <QtWidgets/QApplication>
#include <QtWidgets/QWidget>

#include <algorithm>
#include <cstdlib>
#include <cstring>
#include <map>
#include <memory>
#include <stdexcept>
#include <typeinfo>
#include <vector>

#ifndef _MSC_VER
#include <cxxabi.h>
#endif // !_MSC_VER

namespace Ovygram::Widgets {
namespace {

constexpr auto kHandleProperty = "_ovygram_handle";
constexpr auto kMaximumTreeNodes = 3000;
constexpr auto kMaximumDepth = 32;

struct Selector {
	QString className;
	QString ancestor;
	QString name;
	QString accessible;
	QString element;
	int index = -1;
};

struct Rule {
	QString pluginId;
	Selector selector;
	QString action; // "hide" or "click".
	bool replace = false;
	std::vector<QPointer<QWidget>> hidden; // Hidden by this rule, to restore.
};

struct KeyRule {
	QString pluginId;
	QKeySequence sequence;
	QString element; // Only while the focus is inside this element.
	bool replace = false;
};

class Filter final : public QObject {
protected:
	bool eventFilter(QObject *watched, QEvent *e) override;
};

struct State {
	std::map<quint64, QPointer<QWidget>> handles;
	quint64 nextHandle = 0;
	std::map<QString, Rule> rules; // Rule ID -> rule.
	std::map<QString, KeyRule> keys; // Rule ID -> key rule.
	std::function<void(QJsonObject)> send;
	std::unique_ptr<Filter> filter;
	struct KeyIdentity {
		const QEvent *event = nullptr;
		quint64 timestamp = 0;
		int key = 0;
		int modifiers = 0;

		friend bool operator==(const KeyIdentity &, const KeyIdentity &) = default;
	};
	KeyIdentity lastKey;
};

State &Get() {
	// Leaked on purpose: the filter must outlive every widget.
	static const auto result = new State();
	return *result;
}

[[nodiscard]] QString ClassName(const QWidget *widget) {
	const auto raw = typeid(*widget).name();
#ifdef _MSC_VER
	auto result = QString::fromLatin1(raw);
	for (const auto prefix : { "class ", "struct " }) {
		if (result.startsWith(QLatin1String(prefix))) {
			result = result.mid(int(strlen(prefix)));
		}
	}
	return result;
#else // _MSC_VER
	auto status = 0;
	const auto demangled = abi::__cxa_demangle(raw, nullptr, nullptr, &status);
	const auto result = QString::fromLatin1(
		(status == 0 && demangled) ? demangled : raw);
	std::free(demangled);
	return result;
#endif // _MSC_VER
}

quint64 HandleOf(QWidget *widget) {
	const auto existing = widget->property(kHandleProperty);
	if (existing.isValid()) {
		return existing.toULongLong();
	}
	auto &state = Get();
	const auto handle = ++state.nextHandle;
	state.handles.emplace(handle, widget);
	widget->setProperty(kHandleProperty, handle);
	return handle;
}

[[nodiscard]] Selector ParseSelector(const QJsonObject &value) {
	auto result = Selector{
		.className = value.value(u"cls"_q).toString(),
		.ancestor = value.value(u"ancestor"_q).toString(),
		.name = value.value(u"name"_q).toString(),
		.accessible = value.value(u"accessible"_q).toString(),
		.element = value.value(u"element"_q).toString(),
		.index = value.value(u"index"_q).toInt(-1),
	};
	if (result.className.isEmpty() && result.name.isEmpty()
		&& result.accessible.isEmpty() && result.element.isEmpty()) {
		throw std::runtime_error(
			"A selector needs cls, name, accessible or element.");
	}
	return result;
}

[[nodiscard]] bool MatchesSelf(QWidget *widget, const Selector &selector) {
	if (!selector.className.isEmpty()
		&& ClassName(widget) != selector.className) {
		return false;
	} else if (!selector.name.isEmpty()
		&& widget->objectName() != selector.name) {
		return false;
	} else if (!selector.accessible.isEmpty()
		&& widget->accessibleName() != selector.accessible) {
		return false;
	} else if (!selector.element.isEmpty()
		&& widget->property("_ovygram_element").toString() != selector.element) {
		return false;
	} else if (!selector.ancestor.isEmpty()) {
		auto parent = widget->parentWidget();
		while (parent && ClassName(parent) != selector.ancestor) {
			parent = parent->parentWidget();
		}
		if (!parent) {
			return false;
		}
	}
	return true;
}

[[nodiscard]] bool Matches(QWidget *widget, const Selector &selector) {
	if (!MatchesSelf(widget, selector)) {
		return false;
	} else if (selector.index < 0) {
		return true;
	}
	// index counts matching siblings under the same parent.
	const auto parent = widget->parentWidget();
	if (!parent) {
		return selector.index == 0;
	}
	auto index = 0;
	for (const auto child : parent->children()) {
		const auto sibling = qobject_cast<QWidget*>(child);
		if (!sibling || !MatchesSelf(sibling, selector)) {
			continue;
		} else if (sibling == widget) {
			return index == selector.index;
		}
		++index;
	}
	return false;
}

[[nodiscard]] Rule *HidingRule(QWidget *widget) {
	for (auto &[id, rule] : Get().rules) {
		if (rule.action == u"hide"_q && Matches(widget, rule.selector)) {
			return &rule;
		}
	}
	return nullptr;
}

[[nodiscard]] bool HiddenByRule(QWidget *widget) {
	return HidingRule(widget) != nullptr;
}

void HideMatching(QWidget *widget) {
	if (widget->isHidden()) {
		return;
	} else if (const auto rule = HidingRule(widget)) {
		widget->hide();
		const auto known = std::find(
			begin(rule->hidden),
			end(rule->hidden),
			widget);
		if (known == end(rule->hidden)) {
			rule->hidden.emplace_back(widget);
		}
	}
}

// Shows what removed rules hid, unless another rule still hides it.
void Restore(std::vector<QPointer<QWidget>> hidden) {
	for (const auto &widget : hidden) {
		if (widget && widget->isHidden() && !HiddenByRule(widget.data())) {
			widget->show();
		}
	}
}

void ApplyToAll() {
	for (const auto widget : QApplication::allWidgets()) {
		HideMatching(widget);
	}
}

void EnsureFilter() {
	auto &state = Get();
	if (!state.filter) {
		state.filter = std::make_unique<Filter>();
		qApp->installEventFilter(state.filter.get());
	}
}

void Send(const QString &pluginId, const QString &type, const QString &ruleId) {
	if (const auto &send = Get().send) {
		send(QJsonObject{
			{ u"plugin_id"_q, pluginId },
			{ u"type"_q, type },
			{ u"rule_id"_q, ruleId },
		});
	}
}

[[nodiscard]] bool InsideElement(QObject *watched, const QString &element) {
	if (element.isEmpty()) {
		return true;
	}
	for (auto widget = qobject_cast<QWidget*>(watched); widget;
			widget = widget->parentWidget()) {
		if (widget->property("_ovygram_element").toString() == element) {
			return true;
		}
	}
	return false;
}

// Key rules that match this key event in this widget.
[[nodiscard]] std::vector<std::pair<QString, QString>> MatchingKeys(
		QObject *watched,
		QKeyEvent *key,
		bool &replace) {
	auto result = std::vector<std::pair<QString, QString>>();
	const auto pressed = QKeySequence(key->keyCombination());
	for (const auto &[id, rule] : Get().keys) {
		if (rule.sequence.matches(pressed) == QKeySequence::ExactMatch
			&& InsideElement(watched, rule.element)) {
			replace = replace || rule.replace;
			result.emplace_back(rule.pluginId, id);
		}
	}
	return result;
}

bool Filter::eventFilter(QObject *watched, QEvent *e) {
	const auto type = e->type();
	auto &state = Get();
	if (type == QEvent::ShortcutOverride && !state.keys.empty()) {
		// Accepting the override delivers the key as a KeyPress instead of
		// triggering a Telegram shortcut, so a replacing rule wins.
		auto replace = false;
		const auto key = static_cast<QKeyEvent*>(e);
		if (qobject_cast<QWidget*>(watched)
			&& !MatchingKeys(watched, key, replace).empty()
			&& replace) {
			e->accept();
			return true;
		}
		return false;
	}
	if (type == QEvent::Show) {
		if (const auto widget = qobject_cast<QWidget*>(watched)) {
			if (!state.rules.empty() && HiddenByRule(widget)) {
				const auto weak = QPointer<QWidget>(widget);
				QMetaObject::invokeMethod(this, [=] {
					if (weak) {
						HideMatching(weak.data());
					}
				}, Qt::QueuedConnection);
			}
		}
	} else if (type == QEvent::MouseButtonPress
		|| type == QEvent::MouseButtonRelease) {
		const auto widget = qobject_cast<QWidget*>(watched);
		const auto mouse = static_cast<QMouseEvent*>(e);
		if (!widget || mouse->button() != Qt::LeftButton) {
			return false;
		}
		auto replace = false;
		auto matched = std::vector<std::pair<QString, QString>>();
		for (const auto &[id, rule] : state.rules) {
			if (rule.action == u"click"_q && Matches(widget, rule.selector)) {
				replace = replace || rule.replace;
				matched.emplace_back(rule.pluginId, id);
			}
		}
		if (type == QEvent::MouseButtonRelease
			&& widget->rect().contains(mouse->position().toPoint())) {
			for (const auto &[pluginId, id] : matched) {
				Send(pluginId, u"widget_click"_q, id);
			}
		}
		return replace;
	} else if (type == QEvent::KeyPress && !state.keys.empty()) {
		const auto key = static_cast<QKeyEvent*>(e);
		// A key event travels from the focus widget up its parents as the
		// same object; QWindow gets a separate one. Handle each event once.
		// The address alone isn't enough: Qt creates key events on the
		// stack, so every press usually has the same address.
		const auto identity = State::KeyIdentity{
			.event = e,
			.timestamp = key->timestamp(),
			.key = key->key(),
			.modifiers = int(key->modifiers()),
		};
		if (key->isAutoRepeat()
			|| !qobject_cast<QWidget*>(watched)
			|| state.lastKey == identity) {
			return false;
		}
		state.lastKey = identity;
		auto replace = false;
		const auto matched = MatchingKeys(watched, key, replace);
		if (!matched.empty()) {
			for (const auto &[pluginId, id] : matched) {
				Send(pluginId, u"key"_q, id);
			}
			// Delivered to every widget on the way, so report it once.
			return replace;
		}
	}
	return false;
}

[[nodiscard]] QJsonValue ToJson(const QVariant &value) {
	switch (value.typeId()) {
	case QMetaType::QRect: {
		const auto rect = value.toRect();
		return QJsonArray{ rect.x(), rect.y(), rect.width(), rect.height() };
	}
	case QMetaType::QSize: {
		const auto size = value.toSize();
		return QJsonArray{ size.width(), size.height() };
	}
	case QMetaType::QPoint: {
		const auto point = value.toPoint();
		return QJsonArray{ point.x(), point.y() };
	}
	}
	const auto json = QJsonValue::fromVariant(value);
	return json.isNull() ? QJsonValue(value.toString()) : json;
}

[[nodiscard]] QVariant FromJson(const QJsonValue &value, int typeId) {
	const auto list = value.toArray();
	switch (typeId) {
	case QMetaType::QRect:
		return QRect(list.at(0).toInt(), list.at(1).toInt(),
			list.at(2).toInt(), list.at(3).toInt());
	case QMetaType::QSize:
		return QSize(list.at(0).toInt(), list.at(1).toInt());
	case QMetaType::QPoint:
		return QPoint(list.at(0).toInt(), list.at(1).toInt());
	}
	auto result = value.toVariant();
	if (!result.convert(QMetaType(typeId))) {
		throw std::runtime_error("The value doesn't fit the property type.");
	}
	return result;
}

QJsonObject Describe(QWidget *widget, int depth, int maxDepth, int &count) {
	++count;
	const auto geometry = widget->geometry();
	auto result = QJsonObject{
		{ u"handle"_q, QString::number(HandleOf(widget)) },
		{ u"cls"_q, ClassName(widget) },
		{ u"visible"_q, widget->isVisible() },
		{ u"geometry"_q, QJsonArray{
			geometry.x(), geometry.y(), geometry.width(), geometry.height() } },
	};
	if (!widget->objectName().isEmpty()) {
		result.insert(u"name"_q, widget->objectName());
	}
	if (!widget->accessibleName().isEmpty()) {
		result.insert(u"accessible"_q, widget->accessibleName());
	}
	const auto element = widget->property("_ovygram_element").toString();
	if (!element.isEmpty()) {
		result.insert(u"element"_q, element);
	}
	if (depth < maxDepth) {
		auto children = QJsonArray();
		for (const auto child : widget->children()) {
			const auto childWidget = qobject_cast<QWidget*>(child);
			if (childWidget && count < kMaximumTreeNodes) {
				children.push_back(Describe(childWidget, depth + 1, maxDepth, count));
			}
		}
		if (!children.isEmpty()) {
			result.insert(u"children"_q, children);
		}
	}
	return result;
}

[[nodiscard]] QWidget *Required(const QJsonValue &handle) {
	const auto result = Resolve(handle);
	if (!result) {
		throw std::runtime_error("The widget no longer exists.");
	}
	return result;
}

} // namespace

QWidget *Resolve(const QJsonValue &handle) {
	auto &handles = Get().handles;
	const auto i = handles.find(handle.toString().toULongLong());
	if (i == end(handles)) {
		return nullptr;
	} else if (!i->second) {
		handles.erase(i);
		return nullptr;
	}
	return i->second.data();
}

void SetEventSender(std::function<void(QJsonObject)> send) {
	Get().send = std::move(send);
}

void Handle(const QJsonObject &command) {
	const auto method = command.value(u"method"_q).toString();
	const auto pluginId = command.value(u"plugin_id"_q).toString();
	const auto ruleId = command.value(u"rule_id"_q).toString();
	auto &state = Get();
	if (method == u"ui.widgets.rule"_q) {
		const auto action = command.value(u"action"_q).toString();
		if (ruleId.isEmpty() || (action != u"hide"_q && action != u"click"_q)) {
			throw std::runtime_error("Invalid widget rule.");
		}
		state.rules[ruleId] = Rule{
			.pluginId = pluginId,
			.selector = ParseSelector(command.value(u"selector"_q).toObject()),
			.action = action,
			.replace = command.value(u"replace"_q).toBool(),
		};
		EnsureFilter();
		if (action == u"hide"_q) {
			ApplyToAll();
		}
	} else if (method == u"ui.widgets.unrule"_q) {
		auto hidden = std::vector<QPointer<QWidget>>();
		if (const auto i = state.rules.find(ruleId); i != end(state.rules)) {
			hidden = std::move(i->second.hidden);
			state.rules.erase(i);
		}
		state.keys.erase(ruleId);
		Restore(std::move(hidden));
	} else if (method == u"ui.keys.add"_q) {
		const auto sequence = QKeySequence(
			command.value(u"sequence"_q).toString(),
			QKeySequence::PortableText);
		if (ruleId.isEmpty() || sequence.isEmpty() || sequence.count() != 1) {
			throw std::runtime_error("Invalid key sequence, use e.g. Ctrl+Shift+K.");
		}
		state.keys[ruleId] = KeyRule{
			.pluginId = pluginId,
			.sequence = sequence,
			.element = command.value(u"element"_q).toString(),
			.replace = command.value(u"replace"_q).toBool(),
		};
		EnsureFilter();
	} else if (method == u"ui.widgets.set"_q) {
		const auto widget = Required(command.value(u"handle"_q));
		const auto name = command.value(u"property"_q).toString().toLatin1();
		const auto meta = widget->metaObject();
		const auto index = meta->indexOfProperty(name.constData());
		if (index < 0 || !meta->property(index).isWritable()) {
			throw std::runtime_error("Unknown or read-only property.");
		}
		const auto property = meta->property(index);
		property.write(
			widget,
			FromJson(command.value(u"value"_q), property.metaType().id()));
	} else {
		throw std::runtime_error("Unknown widgets command.");
	}
}

QJsonValue Request(const QJsonObject &command) {
	const auto method = command.value(u"method"_q).toString();
	if (method == u"widgets.tree"_q) {
		auto root = command.contains(u"root"_q)
			&& !command.value(u"root"_q).isNull()
			? Required(command.value(u"root"_q))
			: QApplication::activeWindow();
		if (!root) {
			const auto windows = QApplication::topLevelWidgets();
			for (const auto window : windows) {
				if (window->isVisible()) {
					root = window;
					break;
				}
			}
		}
		if (!root) {
			return QJsonValue(QJsonValue::Null);
		}
		auto count = 0;
		return Describe(
			root,
			0,
			std::clamp(command.value(u"depth"_q).toInt(8), 1, kMaximumDepth),
			count);
	} else if (method == u"widgets.get"_q) {
		const auto widget = Required(command.value(u"handle"_q));
		const auto name = command.value(u"property"_q).toString().toLatin1();
		const auto value = widget->property(name.constData());
		if (!value.isValid()) {
			throw std::runtime_error("Unknown property.");
		}
		return ToJson(value);
	}
	throw std::runtime_error("Unknown widgets request.");
}

void RemovePlugin(const QString &pluginId) {
	auto &state = Get();
	auto hidden = std::vector<QPointer<QWidget>>();
	std::erase_if(state.rules, [&](auto &entry) {
		if (entry.second.pluginId != pluginId) {
			return false;
		}
		for (auto &widget : entry.second.hidden) {
			hidden.push_back(std::move(widget));
		}
		return true;
	});
	std::erase_if(state.keys, [&](const auto &entry) {
		return entry.second.pluginId == pluginId;
	});
	Restore(std::move(hidden));
}

} // namespace Ovygram::Widgets
