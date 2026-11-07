#include "ovygram/plugin_elements.h"

#include "ui/style/style_core.h"
#include "ui/style/style_core_palette.h"

#include <QtCore/QCoreApplication>
#include <QtCore/QPointer>
#include <QtGui/QColor>
#include <QtGui/QMouseEvent>
#include <QtGui/QResizeEvent>
#include <QtWidgets/QWidget>

#include <map>
#include <optional>
#include <set>
#include <stdexcept>
#include <vector>

namespace Ovygram {
namespace {

struct Element {
	QString name;
	QPointer<QWidget> widget;
	bool hiddenByRule = false;
	bool wanted = true; // Visibility Telegram asked for while we hid it.
};

struct Rules {
	std::set<QString> hiding; // Plugin IDs.
	std::map<QString, bool> clicks; // Plugin ID -> replace the action.
};

class Filter final : public QObject {
protected:
	bool eventFilter(QObject *watched, QEvent *e) override;
};

struct State {
	std::vector<Element> elements;
	std::map<QString, Rules> rules;
	std::function<void(QJsonObject)> send;
	Filter filter;
	std::optional<QByteArray> palette;
	std::set<QString> paletteOwners;
};

State &Get() {
	// Leaked on purpose: the filter must outlive every watched widget.
	static const auto result = new State();
	return *result;
}

[[nodiscard]] bool Hidden(const QString &name) {
	const auto &rules = Get().rules;
	const auto i = rules.find(name);
	return (i != end(rules)) && !i->second.hiding.empty();
}

void Cleanup() {
	std::erase_if(Get().elements, [](const Element &element) {
		return !element.widget;
	});
}

// Returns true when the visibility changed.
bool Apply(Element &element) {
	const auto widget = element.widget.data();
	if (!widget) {
		return false;
	} else if (Hidden(element.name)) {
		if (!widget->isHidden()) {
			element.wanted = true;
			widget->hide();
			element.hiddenByRule = true;
			return true;
		} else if (!element.hiddenByRule) {
			element.wanted = false;
			element.hiddenByRule = true;
		}
	} else if (element.hiddenByRule) {
		element.hiddenByRule = false;
		if (element.wanted) {
			widget->show();
			return true;
		}
	}
	return false;
}

void Relayout(QWidget *owner) {
	if (owner) {
		// Telegram widgets recompute their layout on resize.
		auto event = QResizeEvent(owner->size(), owner->size());
		QCoreApplication::sendEvent(owner, &event);
	}
}

void ApplyAll(const QString &name) {
	Cleanup();
	auto owners = std::vector<QPointer<QWidget>>();
	for (auto &element : Get().elements) {
		if (element.name == name && Apply(element)) {
			owners.emplace_back(element.widget->parentWidget());
		}
	}
	for (const auto &owner : owners) {
		Relayout(owner.data());
	}
}

[[nodiscard]] Element *Find(QObject *widget) {
	for (auto &element : Get().elements) {
		if (element.widget.data() == widget) {
			return &element;
		}
	}
	return nullptr;
}

bool Filter::eventFilter(QObject *watched, QEvent *e) {
	const auto type = e->type();
	if (type == QEvent::Show) {
		const auto element = Find(watched);
		if (element && Hidden(element->name)) {
			// Shown outside the owner's visibility pass: hide it again.
			const auto widget = element->widget;
			const auto name = element->name;
			QMetaObject::invokeMethod(this, [=] {
				if (widget && Hidden(name) && !widget->isHidden()) {
					ApplyAll(name);
				}
			}, Qt::QueuedConnection);
		}
	} else if (type == QEvent::MouseButtonPress
		|| type == QEvent::MouseButtonRelease) {
		const auto mouse = static_cast<QMouseEvent*>(e);
		const auto element = Find(watched);
		if (!element || mouse->button() != Qt::LeftButton) {
			return false;
		}
		const auto i = Get().rules.find(element->name);
		if (i == end(Get().rules) || i->second.clicks.empty()) {
			return false;
		}
		auto replace = false;
		for (const auto &[pluginId, replaces] : i->second.clicks) {
			replace = replace || replaces;
		}
		const auto inside = element->widget->rect().contains(
			mouse->position().toPoint());
		if (type == QEvent::MouseButtonRelease && inside && Get().send) {
			const auto name = element->name;
			auto plugins = std::vector<QString>();
			for (const auto &[pluginId, replaces] : i->second.clicks) {
				plugins.push_back(pluginId);
			}
			for (const auto &pluginId : plugins) {
				Get().send(QJsonObject{
					{ u"plugin_id"_q, pluginId },
					{ u"type"_q, u"element_click"_q },
					{ u"element"_q, name },
				});
			}
		}
		return replace;
	}
	return false;
}

void SetColors(const QString &pluginId, const QJsonObject &colors) {
	auto &state = Get();
	if (!state.palette) {
		state.palette = style::main_palette::save();
	}
	for (auto i = colors.begin(); i != colors.end(); ++i) {
		const auto color = QColor(i.value().toString());
		if (!color.isValid()) {
			throw std::runtime_error("Invalid color, use #rrggbb or #aarrggbb.");
		}
		const auto name = i.key().toLatin1();
		const auto result = style::main_palette::setColor(
			QLatin1String(name.constData(), name.size()),
			uchar(color.red()),
			uchar(color.green()),
			uchar(color.blue()),
			uchar(color.alpha()));
		if (result == style::palette::SetResult::KeyNotFound) {
			throw std::runtime_error(
				"Unknown palette color: " + i.key().toStdString());
		}
	}
	state.paletteOwners.insert(pluginId);
	style::NotifyPaletteChanged();
}

void ResetColors(const QString &pluginId) {
	auto &state = Get();
	if (!state.paletteOwners.erase(pluginId) || !state.paletteOwners.empty()) {
		return;
	}
	if (state.palette) {
		style::main_palette::load(*state.palette);
		state.palette.reset();
		style::NotifyPaletteChanged();
	}
}

} // namespace

void RegisterElements(
		std::initializer_list<std::pair<const char*, QWidget*>> elements) {
	auto &state = Get();
	Cleanup();
	for (const auto &[name, widget] : elements) {
		if (widget) {
			state.elements.push_back({ QString::fromLatin1(name), widget });
			widget->installEventFilter(&state.filter);
			// Lets generic widget selectors match by element name.
			widget->setProperty("_ovygram_element", QString::fromLatin1(name));
		}
	}
}

void ApplyElementRules(QWidget *owner) {
	Cleanup();
	for (auto &element : Get().elements) {
		if (element.widget && element.widget->parentWidget() == owner) {
			Apply(element);
		}
	}
}

namespace Elements {

void SetEventSender(std::function<void(QJsonObject)> send) {
	Get().send = std::move(send);
}

void Handle(const QJsonObject &command) {
	const auto method = command.value(u"method"_q).toString();
	const auto pluginId = command.value(u"plugin_id"_q).toString();
	const auto name = command.value(u"element"_q).toString();
	if (method == u"ui.element.hide"_q) {
		auto &hiding = Get().rules[name].hiding;
		if (command.value(u"hidden"_q).toBool()) {
			hiding.insert(pluginId);
		} else {
			hiding.erase(pluginId);
		}
		ApplyAll(name);
	} else if (method == u"ui.element.click"_q) {
		auto &clicks = Get().rules[name].clicks;
		if (command.value(u"enabled"_q).toBool()) {
			clicks[pluginId] = command.value(u"replace"_q).toBool();
		} else {
			clicks.erase(pluginId);
		}
	} else if (method == u"ui.palette"_q) {
		if (command.value(u"reset"_q).toBool()) {
			ResetColors(pluginId);
		} else {
			SetColors(pluginId, command.value(u"colors"_q).toObject());
		}
	} else {
		throw std::runtime_error("Unknown UI element command.");
	}
}

void RemovePlugin(const QString &pluginId) {
	auto changed = std::vector<QString>();
	for (auto &[name, rules] : Get().rules) {
		rules.clicks.erase(pluginId);
		if (rules.hiding.erase(pluginId)) {
			changed.push_back(name);
		}
	}
	for (const auto &name : changed) {
		ApplyAll(name);
	}
	ResetColors(pluginId);
}

} // namespace Elements
} // namespace Ovygram
