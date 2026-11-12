#include "ovygram/plugin_elements.h"

#include "ui/style/style_core.h"
#include "ui/widgets/fields/input_field.h"

#include <QtGui/QTextCursor>
#include <QtGui/QTextDocument>
#include <QtWidgets/QTextEdit>
#include "ui/style/style_core_palette.h"

#include <QtCore/QCoreApplication>
#include <QtCore/QPointer>
#include <QtGui/QColor>
#include <QtGui/QMouseEvent>
#include <QtGui/QResizeEvent>
#include <QtWidgets/QApplication>
#include <QtWidgets/QWidget>

#include <map>
#include <optional>
#include <set>
#include <stdexcept>
#include <utility>
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
	std::map<QString, QString> composeWatchers; // Rule ID -> plugin ID.
	bool editing = false; // Applying a plugin's compose command.
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
		for (const auto &[installationId, replaces] : i->second.clicks) {
			replace = replace || replaces;
		}
		const auto inside = element->widget->rect().contains(
			mouse->position().toPoint());
		if (type == QEvent::MouseButtonRelease && inside && Get().send) {
			const auto name = element->name;
			auto plugins = std::vector<QString>();
			for (const auto &[installationId, replaces] : i->second.clicks) {
				plugins.push_back(installationId);
			}
			for (const auto &installationId : plugins) {
				Get().send(QJsonObject{
					{ u"installation_id"_q, installationId },
					{ u"type"_q, u"element_click"_q },
					{ u"element"_q, name },
				});
			}
		}
		return replace;
	}
	return false;
}

// The element shown in the active window, or any shown one.
[[nodiscard]] QWidget *FindShown(const QString &name) {
	Cleanup();
	auto fallback = (QWidget*)nullptr;
	for (const auto &element : Get().elements) {
		const auto widget = element.widget.data();
		if (element.name != name || !widget || !widget->isVisible()) {
			continue;
		} else if (widget->isActiveWindow()) {
			return widget;
		} else if (!fallback) {
			fallback = widget;
		}
	}
	return fallback;
}

// QTextDocument positions count UTF-16 code units, Python indexes str by
// code points: an emoji outside the BMP is 2 units and 1 code point.
[[nodiscard]] int UnitsToCodePoints(const QString &text, int units) {
	units = std::clamp(units, 0, int(text.size()));
	auto result = 0;
	for (auto i = 0; i < units; ++i, ++result) {
		if (text[i].isHighSurrogate()
			&& i + 1 < text.size()
			&& text[i + 1].isLowSurrogate()) {
			++i;
		}
	}
	return result;
}

[[nodiscard]] int CodePointsToUnits(const QString &text, int points) {
	auto i = 0;
	for (; i < text.size() && points > 0; ++i, --points) {
		if (text[i].isHighSurrogate()
			&& i + 1 < text.size()
			&& text[i + 1].isLowSurrogate()) {
			++i;
		}
	}
	return i;
}

// Text is the document text (custom emoji are U+FFFC there), positions are
// code point indexes into it, as Python str indexes.
[[nodiscard]] QJsonObject FieldState(not_null<Ui::InputField*> field) {
	const auto cursor = field->textCursor();
	const auto text = field->rawTextEdit()->toPlainText();
	return {
		{ u"text"_q, text },
		{ u"cursor"_q, UnitsToCodePoints(text, cursor.position()) },
		{ u"selection_start"_q, UnitsToCodePoints(text, cursor.selectionStart()) },
		{ u"selection_end"_q, UnitsToCodePoints(text, cursor.selectionEnd()) },
	};
}

void WatchField(not_null<Ui::InputField*> field) {
	field->changes() | rpl::on_next([=] {
		auto &state = Get();
		// Only edits by the user: the focus is on the inner QTextEdit.
		if (state.composeWatchers.empty()
			|| !state.send
			|| state.editing
			|| !field->rawTextEdit()->hasFocus()) {
			return;
		}
		const auto value = FieldState(field);
		const auto watchers = state.composeWatchers;
		for (const auto &[ruleId, installationId] : watchers) {
			state.send(QJsonObject{
				{ u"installation_id"_q, installationId },
				{ u"type"_q, u"compose_changed"_q },
				{ u"rule_id"_q, ruleId },
				{ u"value"_q, value },
			});
		}
	}, field->lifetime());
}

[[nodiscard]] Ui::InputField *ComposeField() {
	const auto result = dynamic_cast<Ui::InputField*>(
		FindShown(u"compose.field"_q));
	if (!result) {
		throw std::runtime_error("No message field is shown.");
	}
	return result;
}

void SetColors(const QString &installationId, const QJsonObject &colors) {
	auto &state = Get();
	auto parsed = std::vector<std::pair<QByteArray, QColor>>();
	for (auto i = colors.begin(); i != colors.end(); ++i) {
		const auto color = QColor(i.value().toString());
		if (!color.isValid()) {
			throw std::runtime_error("Invalid color, use #rrggbb or #aarrggbb.");
		}
		parsed.emplace_back(i.key().toLatin1(), color);
	}
	// All or nothing: an unknown name undoes the colors set before it.
	const auto before = style::main_palette::save();
	for (const auto &[name, color] : parsed) {
		const auto result = style::main_palette::setColor(
			QLatin1String(name.constData(), name.size()),
			uchar(color.red()),
			uchar(color.green()),
			uchar(color.blue()),
			uchar(color.alpha()));
		if (result == style::palette::SetResult::KeyNotFound) {
			style::main_palette::load(before);
			throw std::runtime_error(
				"Unknown palette color: " + name.toStdString());
		}
	}
	if (!state.palette) {
		state.palette = before;
	}
	state.paletteOwners.insert(installationId);
	style::NotifyPaletteChanged();
}

void ResetColors(const QString &installationId) {
	auto &state = Get();
	if (!state.paletteOwners.erase(installationId) || !state.paletteOwners.empty()) {
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
			if (const auto field = dynamic_cast<Ui::InputField*>(widget)) {
				WatchField(field);
			}
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
	const auto installationId = command.value(u"installation_id"_q).toString();
	const auto name = command.value(u"element"_q).toString();
	// Edits made by plugin commands aren't reported back as user edits, so a
	// plugin reacting to changes can't loop on its own edits.
	auto &editing = Get().editing;
	const auto wasEditing = std::exchange(editing, true);
	const auto restore = gsl::finally([&] { editing = wasEditing; });
	if (method == u"ui.element.hide"_q) {
		auto &hiding = Get().rules[name].hiding;
		if (command.value(u"hidden"_q).toBool()) {
			hiding.insert(installationId);
		} else {
			hiding.erase(installationId);
		}
		ApplyAll(name);
	} else if (method == u"ui.element.click"_q) {
		auto &clicks = Get().rules[name].clicks;
		if (command.value(u"enabled"_q).toBool()) {
			clicks[installationId] = command.value(u"replace"_q).toBool();
		} else {
			clicks.erase(installationId);
		}
	} else if (method == u"ui.compose.set"_q) {
		const auto field = ComposeField();
		const auto text = command.value(u"text"_q).toString();
		field->setTextWithTags({ text, {} });
		field->setCursorPosition(text.size());
		field->setFocus();
	} else if (method == u"ui.compose.insert"_q) {
		const auto field = ComposeField();
		field->insertTag(command.value(u"text"_q).toString());
		field->setFocus();
	} else if (method == u"ui.compose.replace"_q) {
		const auto field = ComposeField();
		const auto edit = field->rawTextEdit();
		auto cursor = edit->textCursor();
		// Python sends code point indexes, see FieldState().
		const auto current = edit->toPlainText();
		const auto from = CodePointsToUnits(
			current,
			command.value(u"start"_q).toInt());
		const auto till = std::max(
			CodePointsToUnits(current, command.value(u"end"_q).toInt()),
			from);
		const auto text = command.value(u"text"_q).toString();
		cursor.setPosition(from);
		cursor.setPosition(till, QTextCursor::KeepAnchor);
		cursor.insertText(text);
		if (command.value(u"select"_q).toBool()) {
			cursor.setPosition(from);
			cursor.setPosition(from + int(text.size()), QTextCursor::KeepAnchor);
		}
		edit->setTextCursor(cursor);
	} else if (method == u"ui.compose.watch"_q) {
		const auto ruleId = command.value(u"rule_id"_q).toString();
		if (command.value(u"enabled"_q).toBool()) {
			Get().composeWatchers[ruleId] = installationId;
		} else {
			Get().composeWatchers.erase(ruleId);
		}
	} else if (method == u"ui.palette"_q) {
		if (command.value(u"reset"_q).toBool()) {
			ResetColors(installationId);
		} else {
			SetColors(installationId, command.value(u"colors"_q).toObject());
		}
	} else {
		throw std::runtime_error("Unknown UI element command.");
	}
}

QJsonValue Request(const QJsonObject &command) {
	const auto method = command.value(u"method"_q).toString();
	const auto field = dynamic_cast<Ui::InputField*>(
		FindShown(u"compose.field"_q));
	if (method == u"compose.get_text"_q) {
		return field
			? QJsonValue(field->getTextWithTags().text)
			: QJsonValue(QJsonValue::Null);
	} else if (method == u"compose.get_state"_q) {
		return field ? QJsonValue(FieldState(field)) : QJsonValue(QJsonValue::Null);
	}
	throw std::runtime_error("Unknown element request.");
}

void RemovePlugin(const QString &installationId) {
	std::erase_if(Get().composeWatchers, [&](const auto &entry) {
		return entry.second == installationId;
	});
	auto changed = std::vector<QString>();
	for (auto &[name, rules] : Get().rules) {
		rules.clicks.erase(installationId);
		if (rules.hiding.erase(installationId)) {
			changed.push_back(name);
		}
	}
	for (const auto &name : changed) {
		ApplyAll(name);
	}
	ResetColors(installationId);
}

} // namespace Elements
} // namespace Ovygram
