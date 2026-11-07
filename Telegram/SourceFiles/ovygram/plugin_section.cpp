#include "ovygram/plugin_section.h"

#include "ovygram/plugin_ui.h"

#include "ui/painter.h"
#include "ui/rp_widget.h"
#include "ui/widgets/buttons.h"
#include "ui/widgets/labels.h"
#include "ui/widgets/scroll_area.h"
#include "window/section_memento.h"
#include "window/section_widget.h"
#include "window/window_session_controller.h"
#include "styles/style_info.h"
#include "styles/style_layers.h"

#include <QtCore/QPointer>

#include <map>
#include <memory>

namespace Ovygram {
namespace {

// Shared by the shown section and the mementos of it in the window
// history. When the last of them is gone, nothing can show the section
// again, so the surface is closed.
struct Token {
	QString objectId;
	QPointer<PluginUi> ui;

	~Token() {
		if (const auto raw = ui.data()) {
			raw->sectionGone(objectId);
		}
	}
};

[[nodiscard]] std::shared_ptr<Token> TokenFor(const QString &objectId) {
	static auto tokens = std::map<QString, std::weak_ptr<Token>>();
	std::erase_if(tokens, [](const auto &entry) {
		return entry.second.expired();
	});
	if (const auto existing = tokens[objectId].lock()) {
		return existing;
	}
	// Filled in place: a temporary Token would close the surface when
	// destroyed.
	auto result = std::make_shared<Token>();
	result->objectId = objectId;
	result->ui = PluginUi::Instance();
	tokens[objectId] = result;
	return result;
}

class Section final : public Window::SectionWidget {
public:
	Section(
		QWidget *parent,
		not_null<Window::SessionController*> controller,
		std::shared_ptr<Token> token);
	~Section();

	[[nodiscard]] const QString &objectId() const {
		return _token->objectId;
	}

	bool showInternal(
		not_null<Window::SectionMemento*> memento,
		const Window::SectionShow &params) override;
	std::shared_ptr<Window::SectionMemento> createMemento() override;

	bool floatPlayerHandleWheelEvent(QEvent *e) override;
	QRect floatPlayerAvailableRect() override;

protected:
	void resizeEvent(QResizeEvent *e) override;
	void paintEvent(QPaintEvent *e) override;

private:
	void updateControlsGeometry();

	const std::shared_ptr<Token> _token;
	const not_null<Ui::IconButton*> _back;
	const not_null<Ui::FlatLabel*> _title;
	const not_null<Ui::ScrollArea*> _scroll;
	const not_null<Ui::RpWidget*> _holder;
	QPointer<Ui::RpWidget> _content;

};

class Memento final : public Window::SectionMemento {
public:
	explicit Memento(std::shared_ptr<Token> token)
	: _token(std::move(token)) {
	}

	object_ptr<Window::SectionWidget> createWidget(
			QWidget *parent,
			not_null<Window::SessionController*> controller,
			Window::Column column,
			const QRect &geometry) override {
		if (column == Window::Column::Third) {
			return nullptr;
		}
		auto result = object_ptr<Section>(parent, controller, _token);
		result->setGeometry(geometry);
		return result;
	}

	// The window history drops the memento when the plugin closes it.
	rpl::producer<> removeRequests() const override {
		const auto ui = PluginUi::Instance();
		return ui
			? ui->sectionClosed(_token->objectId)
			: rpl::single(rpl::empty);
	}

	[[nodiscard]] const QString &objectId() const {
		return _token->objectId;
	}

private:
	const std::shared_ptr<Token> _token;

};

Section::Section(
	QWidget *parent,
	not_null<Window::SessionController*> controller,
	std::shared_ptr<Token> token)
: SectionWidget(parent, controller)
, _token(std::move(token))
, _back(Ui::CreateChild<Ui::IconButton>(this, st::infoTopBarBack))
, _title(Ui::CreateChild<Ui::FlatLabel>(this, st::infoTopBarTitle))
, _scroll(Ui::CreateChild<Ui::ScrollArea>(this, st::boxScroll))
, _holder(_scroll->setOwnedWidget(object_ptr<Ui::RpWidget>(_scroll)).data()) {
	_back->setClickedCallback([=] {
		controller->showBackFromStack();
	});
	const auto ui = PluginUi::Instance();
	if (!ui) {
		return;
	}
	_title->setText(ui->sectionTitle(objectId()));
	_content = ui->sectionContent(objectId());
	if (const auto content = _content.data()) {
		content->setParent(_holder);
		content->show();
		content->heightValue() | rpl::on_next([=](int height) {
			_holder->resize(_holder->width(), height);
		}, _holder->lifetime());
	}
	ui->sectionClosed(objectId()) | rpl::on_next([=] {
		// Not from inside the plugin command that closed it.
		crl::on_main(this, [=] {
			controller->showBackFromStack();
		});
	}, lifetime());
}

Section::~Section() {
	// The content belongs to the surface: keep it for the next showing.
	if (const auto content = _content.data()) {
		content->hide();
		content->setParent(nullptr);
	}
}

bool Section::showInternal(
		not_null<Window::SectionMemento*> memento,
		const Window::SectionShow &params) {
	const auto same = dynamic_cast<Memento*>(memento.get());
	return same && (same->objectId() == objectId());
}

std::shared_ptr<Window::SectionMemento> Section::createMemento() {
	return std::make_shared<Memento>(_token);
}

bool Section::floatPlayerHandleWheelEvent(QEvent *e) {
	return _scroll->viewportEvent(e);
}

QRect Section::floatPlayerAvailableRect() {
	return mapToGlobal(_scroll->geometry());
}

void Section::resizeEvent(QResizeEvent *e) {
	updateControlsGeometry();
}

void Section::updateControlsGeometry() {
	const auto top = st::infoTopBarHeight;
	_back->moveToLeft(0, 0, width());
	const auto left = _back->width();
	_title->resizeToWidth(std::max(width() - left - st::boxRowPadding.right(), 1));
	_title->moveToLeft(left, (top - _title->height()) / 2, width());
	_scroll->setGeometry(0, top, width(), std::max(height() - top, 0));
	_holder->resize(_scroll->width(), _holder->height());
	if (const auto content = _content.data()) {
		content->resizeToWidth(_scroll->width());
	}
}

void Section::paintEvent(QPaintEvent *e) {
	auto p = QPainter(this);
	p.fillRect(e->rect(), st::windowBg);
	p.fillRect(
		0,
		st::infoTopBarHeight - st::lineWidth,
		width(),
		st::lineWidth,
		st::shadowFg);
}

} // namespace

void ShowPluginSection(
		not_null<Window::SessionController*> controller,
		const QString &objectId) {
	controller->showSection(std::make_shared<Memento>(TokenFor(objectId)));
}

} // namespace Ovygram
