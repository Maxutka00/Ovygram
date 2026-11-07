#include "ovygram/plugin_ui.h"

#include "ovygram/chat_bars.h"
#include "ovygram/chat_decorations.h"
#include "ovygram/chat_list_filter.h"
#include "ovygram/message_decorations.h"
#include "ovygram/plugin_elements.h"
#include "ovygram/plugin_paint.h"
#include "ovygram/plugin_widgets.h"

#include "base/algorithm.h"
#include "base/unique_qptr.h"
#include "core/application.h"
#include "data/data_peer.h"
#include "main/main_session.h"
#include "ui/layers/generic_box.h"
#include "ui/layers/show.h"
#include "ui/rp_widget.h"
#include "ui/widgets/buttons.h"
#include "ui/widgets/checkbox.h"
#include "ui/widgets/fields/input_field.h"
#include "ui/widgets/labels.h"
#include "ui/widgets/scroll_area.h"
#include "ui/ui_utility.h"
#include "ui/widgets/separate_panel.h"
#include "ui/wrap/vertical_layout.h"
#include "window/window_controller.h"
#include "styles/style_layers.h"
#include "styles/style_widgets.h"

#include <QtCore/QCoreApplication>
#include <QtCore/QJsonArray>
#include <QtCore/QPointer>
#include <QtGui/QClipboard>
#include <QtGui/QGuiApplication>
#include <QtGui/QImage>
#include <QtGui/QMouseEvent>
#include <QtGui/QPainter>
#include <QtGui/QResizeEvent>

#include <algorithm>
#include <optional>
#include <stdexcept>
#include <utility>

namespace Ovygram {
namespace {

constexpr auto kMaximumDepth = 32;
constexpr auto kMaximumNodes = 2000;
constexpr auto kMaximumCanvasHeight = 4096;
constexpr auto kMaximumCanvasOps = 2000;
constexpr auto kRowSkip = 8;
constexpr auto kColumnSkip = 6;
constexpr auto kBarPadding = 6;

PluginUi *GlobalInstance = nullptr;

// st::boxLabel with another alignment. Kept in static storage, because
// FlatLabel keeps a reference to its style.
[[nodiscard]] const style::FlatLabel &LabelStyle(style::align align) {
	if (align == style::al_topleft) {
		return st::boxLabel;
	}
	static auto center = std::optional<style::FlatLabel>();
	static auto right = std::optional<style::FlatLabel>();
	auto &result = (align == style::al_top) ? center : right;
	if (!result) {
		result.emplace(st::boxLabel);
		result->align = align;
		result->minWidth = 0;
	}
	return *result;
}

class Canvas final : public Ui::RpWidget {
public:
	void setHeight(int height) {
		_height = std::clamp(height, 1, kMaximumCanvasHeight);
	}

	Canvas(QWidget *parent, int height, Fn<void(int, int)> clicked)
	: RpWidget(parent)
	, _height(std::clamp(height, 1, kMaximumCanvasHeight))
	, _clicked(std::move(clicked)) {
		resize(width(), _height);
	}

	void setCommands(const QJsonArray &commands) {
		_ops = ParsePaintOps(commands, kMaximumCanvasOps);
		update();
	}

protected:
	int resizeGetHeight(int newWidth) override {
		return _height;
	}

	void paintEvent(QPaintEvent *e) override {
		auto p = QPainter(this);
		p.setRenderHint(QPainter::Antialiasing);
		PaintOps(p, _ops, rect());
	}

	void mousePressEvent(QMouseEvent *e) override {
		if (_clicked && e->button() == Qt::LeftButton) {
			_clicked(e->pos().x(), e->pos().y());
		}
	}

private:
	int _height = 0;
	const Fn<void(int, int)> _clicked;
	std::vector<PaintOp> _ops;

};

class Picture final : public Ui::RpWidget {
public:
	Picture(QWidget *parent, QImage image, int height)
	: RpWidget(parent)
	, _image(std::move(image))
	, _height(height > 0 ? height : _image.height()) {
		resize(width(), _height);
	}

protected:
	int resizeGetHeight(int newWidth) override {
		return _height;
	}

	void paintEvent(QPaintEvent *e) override {
		auto p = QPainter(this);
		p.setRenderHint(QPainter::SmoothPixmapTransform);
		const auto scaled = _image.size().scaled(
			size(),
			Qt::KeepAspectRatio);
		p.drawImage(QRect(QPoint(), scaled), _image);
	}

private:
	const QImage _image;
	const int _height = 0;

};

// Lays children out horizontally. Each child has a fixed width, its natural
// width ("fit") or a share of the remaining width ("stretch"), and the
// children are aligned vertically inside the row.
class Row final : public Ui::RpWidget {
public:
	struct Size {
		int fixed = -1;
		bool fit = false;
		int stretch = 1;
	};

	Row(QWidget *parent, Qt::Alignment align, int spacing)
	: RpWidget(parent)
	, _align(align)
	, _spacing(spacing) {
	}

	void add(object_ptr<Ui::RpWidget> child, Size size) {
		const auto raw = child.release();
		raw->setParent(this);
		raw->show();
		_children.push_back({ raw, size });
		raw->heightValue(
		) | rpl::skip(1) | rpl::on_next([=] {
			if (!_resizing) {
				resizeToWidth(width());
			}
		}, lifetime());
	}

protected:
	int resizeGetHeight(int newWidth) override {
		std::erase_if(_children, [](const Child &child) {
			return !child.widget;
		});
		const auto count = int(_children.size());
		if (!count) {
			return 0;
		}
		_resizing = true;
		const auto available = std::max(newWidth - _spacing * (count - 1), 0);
		auto widths = std::vector<int>(count, -1);
		auto used = 0;
		auto weights = 0;
		for (auto i = 0; i != count; ++i) {
			const auto &[widget, size] = _children[i];
			if (size.fixed >= 0) {
				widths[i] = size.fixed;
			} else if (size.fit || size.stretch <= 0) {
				widths[i] = natural(widget.data());
			} else {
				weights += size.stretch;
				continue;
			}
			used += widths[i];
		}
		auto remaining = std::max(available - used, 0);
		for (auto i = 0; i != count; ++i) {
			if (widths[i] < 0) {
				const auto stretch = _children[i].size.stretch;
				widths[i] = weights ? (remaining * stretch / weights) : 0;
				remaining -= widths[i];
				weights -= stretch;
			}
		}
		auto height = 0;
		for (auto i = 0; i != count; ++i) {
			const auto &[widget, size] = _children[i];
			const auto button = dynamic_cast<Ui::RoundButton*>(widget.data());
			if (button) {
				// Without an override a button keeps its natural width.
				button->setFullWidth(size.fit ? 0 : std::max(widths[i], 1));
			} else {
				widget->resizeToWidth(std::max(widths[i], 1));
			}
			height = std::max(height, widget->height());
		}
		auto left = 0;
		for (auto i = 0; i != count; ++i) {
			const auto widget = _children[i].widget.data();
			const auto top = (_align & Qt::AlignBottom)
				? (height - widget->height())
				: (_align & Qt::AlignVCenter)
				? (height - widget->height()) / 2
				: 0;
			widget->moveToLeft(left, top, newWidth);
			left += widget->width() + _spacing;
		}
		_resizing = false;
		return height;
	}

private:
	struct Child {
		QPointer<Ui::RpWidget> widget;
		Size size;
	};

	[[nodiscard]] static int natural(not_null<Ui::RpWidget*> widget) {
		if (const auto label = dynamic_cast<Ui::FlatLabel*>(widget.get())) {
			return label->textMaxWidth();
		} else if (dynamic_cast<Ui::RoundButton*>(widget.get())) {
			return widget->width();
		}
		const auto result = widget->naturalWidth();
		return (result > 0) ? result : widget->sizeHint().width();
	}

	const Qt::Alignment _align;
	const int _spacing = 0;
	std::vector<Child> _children;
	bool _resizing = false;

};

// Keeps an overlay canvas over its target widget.
class OverlayWatcher final : public QObject {
public:
	OverlayWatcher(QWidget *target, Canvas *canvas)
	: QObject(canvas)
	, _canvas(canvas) {
		target->installEventFilter(this);
	}

protected:
	bool eventFilter(QObject *watched, QEvent *e) override {
		if (e->type() == QEvent::Resize && _canvas) {
			const auto size = static_cast<QResizeEvent*>(e)->size();
			_canvas->setHeight(size.height());
			_canvas->resize(size);
			_canvas->raise();
		}
		return false;
	}

private:
	const QPointer<Canvas> _canvas;

};

// Background and padding of a plugin bar inside the chat.
class BarFrame final : public Ui::RpWidget {
public:
	BarFrame(object_ptr<Ui::RpWidget> content)
	: RpWidget(nullptr)
	, _content(content.release()) {
		_content->setParent(this);
		_content->show();
	}

protected:
	int resizeGetHeight(int newWidth) override {
		const auto padding = st::boxRowPadding;
		_content->resizeToWidth(
			std::max(newWidth - padding.left() - padding.right(), 1));
		_content->moveToLeft(padding.left(), kBarPadding, newWidth);
		return _content->height() + 2 * kBarPadding;
	}

	void paintEvent(QPaintEvent *e) override {
		auto p = QPainter(this);
		p.fillRect(rect(), st::windowBg);
		p.fillRect(0, height() - st::lineWidth, width(), st::lineWidth, st::shadowFg);
	}

private:
	const QPointer<Ui::RpWidget> _content;

};

} // namespace

int LayoutChatBars(QWidget *chat, PeerData *peer, int left, int top, int width) {
	const auto instance = PluginUi::Instance();
	return instance
		? instance->layoutChatBars(chat, peer, left, top, width)
		: 0;
}

struct PluginUi::Object {
	QString pluginId;
	QString objectId;
	QPointer<Ui::BoxContent> box;
	std::unique_ptr<Ui::SeparatePanel> panel;
	base::unique_qptr<Ui::RpWidget> bar;
	base::unique_qptr<Ui::RpWidget> overlay;
	QString accountId;
	QString chatId;
	std::map<QString, QPointer<QWidget>> nodes;
	std::map<QString, std::shared_ptr<rpl::variable<QString>>> texts;
	int count = 0;
	bool silent = false;
};

PluginUi::PluginUi(EventSender send)
: _send(std::move(send)) {
	GlobalInstance = this;
	Elements::SetEventSender(_send);
	Widgets::SetEventSender(_send);
}

PluginUi *PluginUi::Instance() {
	return GlobalInstance;
}

PluginUi::~PluginUi() {
	if (GlobalInstance == this) {
		GlobalInstance = nullptr;
		Elements::SetEventSender(nullptr);
		Widgets::SetEventSender(nullptr);
	}
	// Surfaces report their destruction to destroyed(), which erases from
	// _objects. Disconnect them first, so destroying _objects can't reenter.
	auto objects = base::take(_objects);
	for (const auto &[id, object] : objects) {
		object->silent = true;
		for (const auto widget : std::initializer_list<QObject*>{
				object->bar.get(),
				object->overlay.get(),
				object->box.data() }) {
			if (widget) {
				QObject::disconnect(widget, nullptr, this, nullptr);
			}
		}
		if (object->box) {
			// The box outlives us during its closing animation; its widgets
			// check the guard in build() before sending events.
			object->box->closeBox();
		}
	}
}

void PluginUi::handle(const QJsonObject &command) {
	const auto method = command.value(u"method"_q).toString();
	if (method == u"ui.show"_q) {
		show(command);
	} else if (method == u"ui.update"_q) {
		update(command);
	} else if (method == u"ui.close"_q) {
		close(command.value(u"object_id"_q).toString(), true);
	} else if (method == u"ui.close_plugin"_q) {
		closePlugin(command.value(u"plugin_id"_q).toString());
		Elements::RemovePlugin(command.value(u"plugin_id"_q).toString());
		Widgets::RemovePlugin(command.value(u"plugin_id"_q).toString());
		Decorations::RemovePlugin(command.value(u"plugin_id"_q).toString());
		ChatListFilter::RemovePlugin(command.value(u"plugin_id"_q).toString());
		MessageDecorations::RemovePlugin(command.value(u"plugin_id"_q).toString());
	} else if (method.startsWith(u"ui.message_decoration."_q)) {
		MessageDecorations::Handle(command);
	} else if (method.startsWith(u"ui.chat_list."_q)) {
		ChatListFilter::Handle(command);
	} else if (method.startsWith(u"ui.decoration."_q)) {
		Decorations::Handle(command);
	} else if (method.startsWith(u"ui.element."_q)
		|| method.startsWith(u"ui.compose."_q)
		|| method == u"ui.palette"_q) {
		Elements::Handle(command);
	} else if (method.startsWith(u"ui.widgets."_q) || method.startsWith(u"ui.keys."_q)) {
		Widgets::Handle(command);
	} else if (method == u"ui.clipboard"_q) {
		QGuiApplication::clipboard()->setText(command.value(u"text"_q).toString());
	} else {
		throw std::runtime_error("Unknown UI command.");
	}
}

void PluginUi::show(const QJsonObject &command) {
	const auto objectId = command.value(u"object_id"_q).toString();
	if (objectId.isEmpty() || _objects.contains(objectId)) {
		throw std::runtime_error("Invalid or repeated object ID.");
	}
	auto owned = std::make_unique<Object>();
	const auto object = owned.get();
	object->pluginId = command.value(u"plugin_id"_q).toString();
	object->objectId = objectId;
	const auto title = command.value(u"title"_q).toString();
	const auto tree = command.value(u"tree"_q).toObject();
	const auto kind = command.value(u"kind"_q).toString();
	if (kind == u"dialog"_q) {
		const auto window = Core::App().activePrimaryWindow();
		if (!window) {
			throw std::runtime_error("No active Telegram window.");
		}
		const auto width = command.value(u"width"_q).toInt();
		// Built before the box, so an invalid tree throws before showing.
		const auto content = std::make_shared<object_ptr<Ui::RpWidget>>(
			build(*object, nullptr, tree, 0));
		auto box = Box([=](not_null<Ui::GenericBox*> box) {
			box->setTitle(rpl::single(title));
			if (width > 0) {
				box->setWidth(std::clamp(width, st::boxWidth, 1200));
			}
			const auto raw = content->data();
			raw->setParent(box);
			box->addRow(std::move(*content));
			raw->show();
			box->addButton(rpl::single(u"Закрыть"_q), [=] {
				box->closeBox();
			});
			if (const auto i = _objects.find(objectId); i != end(_objects)) {
				i->second->box = box.get();
			}
			connect(box.get(), &QObject::destroyed, this, [=] {
				destroyed(objectId);
			});
		});
		_objects.emplace(objectId, std::move(owned));
		window->uiShow()->showBox(std::move(box));
	} else if (kind == u"window"_q) {
		object->panel = std::make_unique<Ui::SeparatePanel>();
		const auto panel = object->panel.get();
		panel->setWindowFlag(Qt::WindowStaysOnTopHint, false);
		panel->setTitle(rpl::single(title));
		panel->setInnerSize(QSize(
			std::clamp(command.value(u"width"_q).toInt(420), 200, 2000),
			std::clamp(command.value(u"height"_q).toInt(480), 120, 2000)),
			true);
		// Content taller than the window scrolls. ScrollArea isn't an
		// RpWidget, so it fills a plain container that the panel shows.
		auto inner = base::make_unique_q<Ui::RpWidget>(panel);
		const auto scroll = Ui::CreateChild<Ui::ScrollArea>(
			inner.get(),
			st::boxScroll);
		inner->sizeValue() | rpl::on_next([=](QSize size) {
			scroll->setGeometry(QRect(QPoint(), size));
		}, inner->lifetime());
		const auto layout = scroll->setOwnedWidget(
			object_ptr<Ui::VerticalLayout>(scroll));
		layout->add(build(*object, layout.data(), tree, 0), st::boxRowPadding);
		scroll->widthValue() | rpl::on_next([=](int width) {
			if (layout) {
				layout->resizeToWidth(width);
			}
		}, layout->lifetime());
		panel->showInner(std::move(inner));
		panel->closeRequests(
		) | rpl::on_next([=] {
			// The panel can't be destroyed from its own signal.
			crl::on_main(this, [=] { close(objectId, true); });
		}, panel->lifetime());
		_objects.emplace(objectId, std::move(owned));
		panel->showAndActivate();
	} else if (kind == u"overlay"_q) {
		const auto target = Widgets::Resolve(command.value(u"target"_q));
		if (!target) {
			throw std::runtime_error("The overlay target no longer exists.");
		} else if (tree.value(u"type"_q).toString() != u"canvas"_q) {
			throw std::runtime_error("An overlay must be a single Canvas.");
		}
		const auto nodeId = tree.value(u"id"_q).toString();
		const auto clickable = command.value(u"clickable"_q).toBool();
		auto canvas = object_ptr<Canvas>(
			target,
			target->height(),
			clickable ? Fn<void(int, int)>([=](int x, int y) {
				if (const auto i = _objects.find(objectId); i != end(_objects)) {
					send(*i->second, nodeId, u"click"_q, QJsonArray{ x, y });
				}
			}) : Fn<void(int, int)>());
		canvas->setCommands(tree.value(u"commands"_q).toArray());
		canvas->setAttribute(Qt::WA_TransparentForMouseEvents, !clickable);
		canvas->setGeometry(target->rect());
		canvas->show();
		canvas->raise();
		new OverlayWatcher(target, canvas.data());
		object->nodes.emplace(nodeId, canvas.data());
		object->overlay = base::unique_qptr<Ui::RpWidget>(canvas.release());
		connect(object->overlay.get(), &QObject::destroyed, this, [=] {
			destroyed(objectId);
		});
		_objects.emplace(objectId, std::move(owned));
	} else if (kind == u"chat_bar"_q) {
		object->accountId = command.value(u"account_id"_q).toString();
		object->chatId = command.value(u"chat_id"_q).toString();
		if (object->accountId.isEmpty() || object->chatId.isEmpty()) {
			throw std::runtime_error("A chat bar needs account_id and chat_id.");
		}
		object->bar = base::unique_qptr<Ui::RpWidget>(
			new BarFrame(build(*object, nullptr, tree, 0)));
		object->bar->hide();
		connect(object->bar.get(), &QObject::destroyed, this, [=] {
			destroyed(objectId);
		});
		_objects.emplace(objectId, std::move(owned));
		relayoutChats();
	} else {
		throw std::runtime_error("Unknown surface kind.");
	}
}

int PluginUi::layoutChatBars(
		QWidget *container,
		PeerData *peer,
		int left,
		int top,
		int width) {
	if (!container) {
		return 0;
	}
	const auto known = std::find_if(begin(_chats), end(_chats), [&](
			const QPointer<QWidget> &chat) {
		return chat.data() == container;
	});
	if (known == end(_chats)) {
		std::erase_if(_chats, [](const QPointer<QWidget> &chat) {
			return !chat;
		});
		_chats.emplace_back(container);
		// A bar lives until the plugin closes it: take it out of a chat
		// that is destroyed. QWidget emits destroyed() before it deletes
		// its children.
		connect(container, &QObject::destroyed, this, [=] {
			for (const auto &[id, object] : _objects) {
				const auto bar = object->bar.get();
				if (bar && bar->parentWidget() == container) {
					bar->hide();
					bar->setParent(nullptr);
				}
			}
		});
	}
	const auto accountId = peer
		? QString::number(peer->session().uniqueId())
		: QString();
	const auto chatId = peer ? QString::number(peer->id.value) : QString();
	auto height = 0;
	for (const auto &[id, object] : _objects) {
		const auto bar = object->bar.get();
		if (!bar) {
			continue;
		} else if (peer
			&& object->accountId == accountId
			&& object->chatId == chatId) {
			if (bar->parentWidget() != container) {
				// On top of the history, but under the panels and menus
				// the chat raises later.
				bar->setParent(container);
				bar->raise();
			}
			bar->resizeToWidth(width);
			bar->moveToLeft(left, top + height, container->width());
			bar->show();
			height += bar->height();
		} else if (bar->parentWidget() == container) {
			bar->hide();
		}
	}
	return height;
}

void PluginUi::relayoutChats() {
	// Deferred: a command can arrive while the chat is still switching
	// peers, and the layout must see the peer it ends up with.
	if (_relayoutQueued) {
		return;
	}
	_relayoutQueued = true;
	crl::on_main(this, [=] {
		_relayoutQueued = false;
		relayoutChatsNow();
	});
}

void PluginUi::relayoutChatsNow() {
	std::erase_if(_chats, [](const QPointer<QWidget> &chat) {
		return !chat;
	});
	for (const auto &chat : _chats) {
		// The chat recomputes its layout, and LayoutChatBars, on resize.
		auto event = QResizeEvent(chat->size(), chat->size());
		QCoreApplication::sendEvent(chat.data(), &event);
	}
}

object_ptr<Ui::RpWidget> PluginUi::build(
		Object &object,
		QWidget *parent,
		const QJsonObject &node,
		int depth) {
	if (depth > kMaximumDepth || ++object.count > kMaximumNodes) {
		throw std::runtime_error("UI tree is too deep or too large.");
	}
	const auto type = node.value(u"type"_q).toString();
	const auto id = node.value(u"id"_q).toString();
	const auto text = node.value(u"text"_q).toString();
	const auto objectId = object.objectId;
	// A dialog belongs to the window, not to us, and can outlive us.
	const auto guard = QPointer<PluginUi>(this);
	const auto sender = [=](const QString &kind, QJsonValue value) {
		if (!guard || _updating) {
			// Changes made by ui.update aren't reported back, so a plugin
			// reacting to them can't loop on its own updates.
			return;
		} else if (const auto i = _objects.find(objectId);
				i != end(_objects) && !i->second->silent) {
			send(*i->second, id, kind, value);
		}
	};
	auto result = object_ptr<Ui::RpWidget>(nullptr);
	if (type == u"column"_q) {
		auto column = object_ptr<Ui::VerticalLayout>(parent);
		for (const auto &child : node.value(u"children"_q).toArray()) {
			column->add(
				build(object, column.data(), child.toObject(), depth + 1),
				QMargins(0, kColumnSkip, 0, kColumnSkip));
		}
		result = std::move(column);
	} else if (type == u"row"_q) {
		const auto align = node.value(u"align"_q).toString(u"center"_q);
		auto row = object_ptr<Row>(
			parent,
			(align == u"top"_q) ? Qt::AlignTop
				: (align == u"bottom"_q) ? Qt::AlignBottom
				: (align == u"center"_q) ? Qt::AlignVCenter
				: throw std::runtime_error("Row align must be top, center or bottom."),
			std::clamp(node.value(u"spacing"_q).toInt(kRowSkip), 0, 200));
		for (const auto &value : node.value(u"children"_q).toArray()) {
			const auto child = value.toObject();
			auto size = Row::Size();
			const auto width = child.value(u"width"_q);
			if (width.isString()) {
				if (width.toString() != u"fit"_q) {
					throw std::runtime_error("Width must be a number or \"fit\".");
				}
				size.fit = true;
			} else if (width.isDouble()) {
				size.fixed = std::clamp(width.toInt(), 0, 4000);
			}
			if (child.contains(u"stretch"_q)) {
				size.stretch = std::clamp(child.value(u"stretch"_q).toInt(), 0, 100);
			}
			row->add(build(object, row.data(), child, depth + 1), size);
		}
		result = std::move(row);
	} else if (type == u"text"_q) {
		const auto align = node.value(u"align"_q).toString(u"left"_q);
		result = object_ptr<Ui::FlatLabel>(
			parent,
			text,
			(align == u"center"_q) ? LabelStyle(style::al_top)
				: (align == u"right"_q) ? LabelStyle(style::al_topright)
				: (align == u"left"_q) ? LabelStyle(style::al_topleft)
				: throw std::runtime_error("Text align must be left, center or right."));
	} else if (type == u"button"_q) {
		const auto value = std::make_shared<rpl::variable<QString>>(text);
		object.texts[id] = value;
		auto button = object_ptr<Ui::RoundButton>(
			parent,
			value->value(),
			st::defaultActiveButton);
		button->setTextTransform(Ui::RoundButtonTextTransform::NoTransform);
		button->setClickedCallback([=] { sender(u"click"_q, QJsonValue()); });
		result = std::move(button);
	} else if (type == u"input"_q) {
		auto field = object_ptr<Ui::InputField>(
			parent,
			st::defaultInputField,
			Ui::InputField::Mode::SingleLine,
			rpl::single(node.value(u"placeholder"_q).toString()),
			TextWithTags{ text });
		const auto raw = field.data();
		raw->changes() | rpl::on_next([=] {
			sender(u"change"_q, raw->getLastText());
		}, raw->lifetime());
		result = std::move(field);
	} else if (type == u"switch"_q) {
		auto box = object_ptr<Ui::Checkbox>(
			parent,
			text,
			node.value(u"value"_q).toBool());
		box->checkedChanges() | rpl::on_next([=](bool checked) {
			sender(u"toggle"_q, checked);
		}, box->lifetime());
		result = std::move(box);
	} else if (type == u"canvas"_q) {
		auto canvas = object_ptr<Canvas>(
			parent,
			node.value(u"height"_q).toInt(),
			[=](int x, int y) { sender(u"click"_q, QJsonArray{ x, y }); });
		canvas->setCommands(node.value(u"commands"_q).toArray());
		result = std::move(canvas);
	} else if (type == u"image"_q) {
		auto image = QImage(node.value(u"path"_q).toString());
		if (image.isNull()) {
			throw std::runtime_error("Image can't be loaded.");
		}
		result = object_ptr<Picture>(
			parent,
			std::move(image),
			node.value(u"height"_q).toInt());
	} else if (type == u"spacer"_q) {
		auto spacer = object_ptr<Ui::RpWidget>(parent);
		spacer->resize(1, std::clamp(node.value(u"height"_q).toInt(), 0, 1000));
		result = std::move(spacer);
	} else {
		throw std::runtime_error("Unknown UI node type.");
	}
	if (id.isEmpty() || object.nodes.contains(id)) {
		throw std::runtime_error("Invalid or repeated node ID.");
	}
	object.nodes.emplace(id, result.data());
	return result;
}

void PluginUi::update(const QJsonObject &command) {
	const auto i = _objects.find(command.value(u"object_id"_q).toString());
	if (i == end(_objects)) {
		return; // Closed meanwhile, Python learns it from the "closed" event.
	}
	const auto &object = *i->second;
	const auto nodeId = command.value(u"node_id"_q).toString();
	const auto node = object.nodes.find(nodeId);
	if (node == end(object.nodes) || !node->second) {
		throw std::runtime_error("Unknown UI node.");
	}
	const auto widget = node->second.data();
	const auto props = command.value(u"props"_q).toObject();
	const auto was = std::exchange(_updating, true);
	const auto restore = gsl::finally([&] { _updating = was; });
	if (props.contains(u"text"_q)) {
		const auto text = props.value(u"text"_q).toString();
		if (const auto label = dynamic_cast<Ui::FlatLabel*>(widget)) {
			label->setText(text);
		} else if (const auto field = dynamic_cast<Ui::InputField*>(widget)) {
			field->setText(text);
		} else if (const auto value = object.texts.find(nodeId);
				value != end(object.texts)) {
			*value->second = text;
		}
	}
	if (props.contains(u"value"_q)) {
		if (const auto box = dynamic_cast<Ui::Checkbox*>(widget)) {
			box->setChecked(
				props.value(u"value"_q).toBool(),
				Ui::Checkbox::NotifyAboutChange::DontNotify);
		}
	}
	if (props.contains(u"commands"_q)) {
		if (const auto canvas = dynamic_cast<Canvas*>(widget)) {
			canvas->setCommands(props.value(u"commands"_q).toArray());
		}
	}
	// An overlay's parent is the Telegram widget it covers: not ours to lay
	// out, and its size doesn't depend on the overlay.
	const auto parent = object.overlay ? nullptr : widget->parentWidget();
	if (const auto rp = dynamic_cast<Ui::RpWidget*>(parent)) {
		rp->resizeToWidth(rp->width());
	}
	if (object.bar) {
		relayoutChats();
	}
}

void PluginUi::close(const QString &objectId, bool notify) {
	const auto i = _objects.find(objectId);
	if (i == end(_objects)) {
		return;
	}
	const auto object = i->second.get();
	object->silent = object->silent || !notify;
	if (object->box) {
		object->box->closeBox(); // destroyed() erases it later.
		return;
	}
	if (!object->silent) {
		send(*object, QString(), u"closed"_q);
	}
	// Deleted after erase(): their destroyed() handler looks up _objects.
	auto bar = std::move(object->bar);
	auto overlay = std::move(object->overlay);
	_objects.erase(i);
	overlay = nullptr;
	if (bar) {
		bar = nullptr;
		relayoutChats();
	}
}

void PluginUi::closePlugin(const QString &pluginId) {
	auto ids = std::vector<QString>();
	for (const auto &[id, object] : _objects) {
		if (object->pluginId == pluginId) {
			ids.push_back(id);
		}
	}
	for (const auto &id : ids) {
		close(id, false);
	}
}

void PluginUi::destroyed(const QString &objectId) {
	const auto i = _objects.find(objectId);
	if (i == end(_objects)) {
		return;
	}
	if (!i->second->silent) {
		send(*i->second, QString(), u"closed"_q);
	}
	i->second->silent = true;
	// QWidget emits destroyed() from its own destructor, before QPointer is
	// cleared, so the bar must be released here, not deleted a second time.
	[[maybe_unused]] const auto released = i->second->bar.release();
	[[maybe_unused]] const auto overlay = i->second->overlay.release();
	_objects.erase(i);
}

void PluginUi::send(
		const Object &object,
		const QString &nodeId,
		const QString &type,
		QJsonValue value) {
	auto event = QJsonObject{
		{ u"plugin_id"_q, object.pluginId },
		{ u"object_id"_q, object.objectId },
		{ u"node_id"_q, nodeId },
		{ u"type"_q, type },
	};
	if (!value.isNull() && !value.isUndefined()) {
		event.insert(u"value"_q, value);
	}
	_send(std::move(event));
}

} // namespace Ovygram
