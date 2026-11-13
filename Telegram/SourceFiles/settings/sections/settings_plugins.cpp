#include "settings/sections/settings_plugins.h"

#include "core/application.h"
#include "core/file_utilities.h"
#include "core/plugin_runtime.h"
#include "ovygram/plugin_install.h"
#include "lang/lang_keys.h"
#include "mainwidget.h"
#include "settings/settings_common_session.h"
#include "ui/boxes/confirm_box.h"
#include "ui/layers/generic_box.h"
#include "ui/painter.h"
#include "ui/search_field_controller.h"
#include "ui/vertical_list.h"
#include "ui/widgets/buttons.h"
#include "ui/widgets/checkbox.h"
#include "ui/widgets/fields/input_field.h"
#include "ui/widgets/labels.h"
#include "ui/wrap/slide_wrap.h"
#include "ui/wrap/vertical_layout.h"
#include "window/window_session_controller.h"
#include "styles/style_boxes.h"
#include "styles/style_layers.h"
#include "styles/style_settings.h"

#include <QtCore/QJsonArray>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonObject>
#include <QtCore/QTimer>
#include <QtCore/QUrl>
#include <QtGui/QDesktopServices>
#include <algorithm>
#include <vector>

namespace Settings {
namespace {

// How often a page refreshes while plugin libraries are installed.
constexpr auto kDependencyPoll = crl::time(1500);
// .ovyplugin and .ovyzip are the plugin formats; the rest import locally.
const auto kPluginFilter = u"Плагины (*.ovyplugin *.ovyzip *.py *.plugin *.zip)"_q;

[[nodiscard]] QJsonValue Request(
		QJsonObject request,
		rpl::variable<QString> &notice) {
	auto error = u"Не удалось запустить встроенный Python. Подробности в журнале клиента."_q;
	if (const auto runtime = Core::App().pluginRuntime()) {
		try {
			const auto response = runtime->dispatch(
				QJsonDocument(request).toJson(QJsonDocument::Compact).toStdString());
			const auto object = QJsonDocument::fromJson(
				QByteArray::fromStdString(response)).object();
			if (object.contains(u"result"_q)) {
				return object.value(u"result"_q);
			}
			error = object.value(u"error"_q).toString(u"Не удалось выполнить действие."_q);
		} catch (const std::exception &exception) {
			error = QString::fromUtf8(exception.what());
		}
	}
	notice = std::move(error);
	return QJsonValue(QJsonValue::Undefined);
}

[[nodiscard]] QString PluginStatus(const QJsonObject &plugin) {
	return plugin.value(u"loaded"_q).toBool()
		? u"Запущен"_q
		: plugin.value(u"enabled"_q).toBool()
		? u"Включён, но не запущен"_q
		: u"Отключён"_q;
}

[[nodiscard]] QString RuntimeStatus(const QJsonObject &snapshot) {
	if (snapshot.value(u"disabled"_q).toBool()) {
		return u"Плагины отключены параметром --disable-plugins."_q;
	} else if (snapshot.value(u"recovery"_q).toBool()) {
		return u"Предыдущий сеанс завершился аварийно. Плагины пока не запущены."_q;
	} else if (snapshot.value(u"restart_required"_q).toBool()) {
		return u"Для дальнейшего запуска плагинов перезапусти клиент."_q;
	}
	return {};
}

not_null<Ui::SettingsButton*> AddAction(
		not_null<Ui::VerticalLayout*> layout,
		QString text,
		Fn<void()> callback,
		const style::SettingsButton &style = st::settingsButtonNoIcon) {
	const auto button = layout->add(object_ptr<Ui::SettingsButton>(
		layout,
		rpl::single(std::move(text)),
		style));
	button->setClickedCallback(std::move(callback));
	return button;
}

void Clear(not_null<Ui::VerticalLayout*> layout) {
	while (layout->count()) {
		delete layout->widgetAt(0);
	}
}

// Keeps the height of a layout while it is rebuilt. An empty layout for a
// moment shrinks the page, and the settings scroll jumps to the top, e.g.
// after toggling a plugin far down the list.
[[nodiscard]] auto HoldHeight(not_null<Ui::VerticalLayout*> layout) {
	layout->setMinimumHeight(layout->height());
	return gsl::finally([=] {
		layout->setMinimumHeight(0);
		layout->resizeToWidth(layout->width());
	});
}

void AddNotice(
		not_null<Ui::VerticalLayout*> layout,
		rpl::variable<QString> &notice) {
	const auto wrap = layout->add(object_ptr<Ui::SlideWrap<Ui::VerticalLayout>>(
		layout,
		object_ptr<Ui::VerticalLayout>(layout)));
	Ui::AddDividerText(wrap->entity(), notice.value());
	wrap->toggleOn(notice.value() | rpl::map([](const QString &text) {
		return !text.isEmpty();
	}));
	wrap->finishAnimating();
}

[[nodiscard]] QString DependencyLine(const QJsonObject &plugin) {
	auto names = QStringList();
	for (const auto &value : plugin.value(u"requirements"_q).toArray()) {
		names.push_back(value.toString());
	}
	if (names.isEmpty()) {
		return QString();
	}
	return (plugin.value(u"installing"_q).toBool()
		? u"Устанавливаются зависимости: "_q
		: u"Зависимости: "_q) + names.join(u", "_q);
}

[[nodiscard]] bool InstallingDependencies(const QJsonObject &snapshot) {
	return !snapshot.value(u"dependencies"_q).toObject().value(
		u"installing"_q).toString().isEmpty();
}

[[nodiscard]] QString DependencyStatus(const QJsonObject &snapshot) {
	return snapshot.value(u"dependencies"_q).toObject().value(u"restart"_q).toBool()
		? u"Новые версии библиотек плагинов применятся после перезапуска клиента."_q
		: QString();
}

[[nodiscard]] QString PluginMetadata(const QJsonObject &plugin) {
	auto result = u"Версия %1 · %2 · %3"_q.arg(
		plugin.value(u"version"_q).toString().simplified(),
		plugin.value(u"display_author"_q).toString(plugin.value(u"author"_q).toString()).simplified(),
		plugin.value(u"plugin_id"_q).toString());
	// Installations of one plugin ID differ by their installation_id.
	if (plugin.value(u"instances"_q).toInt() > 1) {
		result += u" · экземпляр %1"_q.arg(
			plugin.value(u"installation_id"_q).toString().left(8));
	}
	return result;
}

[[nodiscard]] QString TrustStatus(const QJsonObject &plugin) {
	const auto status = plugin.value(u"trust"_q).toObject().value(u"status"_q).toString();
	if (status == u"verified"_q) return u"Проверенный плагин"_q;
	if (status == u"official"_q) return u"Официальный плагин"_q;
	if (status == u"blocked"_q) return u"Опасный плагин / вирус — запуск запрещён"_q;
	if (status == u"revoked"_q) return u"Непроверенный плагин — проверка отозвана"_q;
	if (status == u"verification_unavailable"_q) return u"Сервер не отвечает — невозможно проверить плагин"_q;
	return u"Непроверенный плагин"_q;
}

[[nodiscard]] QString DescriptionPreview(const QString &description) {
	const auto text = description.simplified();
	constexpr auto kLimit = 160;
	return (text.size() > kLimit) ? text.left(kLimit).trimmed() + u"…"_q : text;
}

[[nodiscard]] not_null<Ui::VerticalLayout*> AddCard(
		not_null<Ui::VerticalLayout*> layout) {
	const auto card = layout->add(
		object_ptr<Ui::VerticalLayout>(layout),
		st::settingsPluginCardMargin);
	card->paintRequest() | rpl::on_next([=] {
		auto p = QPainter(card);
		const auto quality = PainterHighQualityEnabler(p);
		p.setPen(Qt::NoPen);
		p.setBrush(st::windowBgOver);
		const auto radius = st::settingsPluginCardRadius;
		p.drawRoundedRect(card->rect(), radius, radius);
	}, card->lifetime());
	return card;
}

not_null<Ui::FlatLabel*> AddCardLabel(
		not_null<Ui::VerticalLayout*> card,
		QString text,
		const style::FlatLabel &style = st::defaultFlatLabel) {
	const auto label = card->add(
		object_ptr<Ui::FlatLabel>(card, std::move(text), style),
		st::settingsPluginTextMargin);
	label->setBreakEverywhere(true);
	return label;
}

void AddTrustMetadata(not_null<Ui::VerticalLayout*> card, const QJsonObject &plugin) {
	const auto author = AddCardLabel(card, PluginMetadata(plugin), st::settingsPluginCardMeta);
	if (plugin.value(u"author_hidden"_q).toBool()) author->setTextColorOverride(QColor(u"#b00020"_q));
	const auto status = plugin.value(u"trust"_q).toObject().value(u"status"_q).toString();
	const auto badge = AddCardLabel(card, TrustStatus(plugin), st::settingsPluginCardMeta);
	badge->setTextColorOverride(QColor(status == u"official"_q ? u"#1565c0"_q
		: status == u"verified"_q ? u"#188038"_q : u"#b00020"_q));
}

class PluginButtonRow final : public Ui::RpWidget {
public:
	PluginButtonRow(QWidget *parent, bool hasToggle = false)
	: Ui::RpWidget(parent)
	, _hasToggle(hasToggle) {
	}

	not_null<Ui::SettingsButton*> addButton(
			QString text,
			const style::SettingsButton &style,
			Fn<void()> action = nullptr) {
		const auto button = Ui::CreateChild<Ui::SettingsButton>(
			this,
			rpl::single(std::move(text)),
			style);
		if (action) {
			button->setClickedCallback(std::move(action));
		}
		button->show();
		_buttons.push_back(button);
		return button;
	}

protected:
	int resizeGetHeight(int width) override {
		const auto count = int(_buttons.size());
		const auto toggleWidth = _hasToggle
			? std::min(width, st::settingsPluginToggleWidth)
			: 0;
		const auto regular = count - (_hasToggle ? 1 : 0);
		const auto space = width - toggleWidth;
		auto left = 0;
		for (auto i = 0; i != count; ++i) {
			const auto right = (i < regular) ? (space * (i + 1) / regular) : width;
			_buttons[i]->resizeToWidth(right - left);
			_buttons[i]->moveToLeft(left, 0, width);
			left = right;
		}
		return st::settingsPluginCardAction.height;
	}

private:
	const bool _hasToggle;
	std::vector<not_null<Ui::SettingsButton*>> _buttons;
};

void AddPluginHeader(
		not_null<Ui::VerticalLayout*> card,
		QString title,
		Fn<void()> open,
		bool enabled,
		bool blocked,
		Fn<void()> toggle) {
	auto row = object_ptr<PluginButtonRow>(card, true);
	row->addButton(std::move(title), st::settingsPluginCardTitle, std::move(open));
	const auto button = row->addButton(
		enabled ? u"Отключить плагин"_q : u"Включить плагин"_q,
		st::settingsPluginCardAction,
		std::move(toggle));
	button->toggleOn(rpl::single(enabled), true);
	button->setDisabled(blocked && !enabled);
	card->add(std::move(row));
}

void AddCardActions(
		not_null<Ui::VerticalLayout*> card,
		Fn<void()> share,
		Fn<void()> remove) {
	auto row = object_ptr<PluginButtonRow>(card);
	row->addButton(u"Отправить"_q, st::settingsPluginCardAction, std::move(share));
	row->addButton(u"Удалить"_q, st::settingsPluginCardRemove, std::move(remove));
	card->add(std::move(row));
}

void ConfirmRemove(
		not_null<Window::SessionController*> controller,
		Fn<void(bool)> remove) {
	controller->show(Box([=](not_null<Ui::GenericBox*> box) {
		box->setTitle(rpl::single(u"Удаление плагина"_q));
		box->addRow(object_ptr<Ui::FlatLabel>(box,
			rpl::single(u"Сохранить настройки и данные этого экземпляра?"_q), st::boxLabel));
		box->addButton(rpl::single(u"Сохранить данные"_q), [=] { box->closeBox(); remove(true); });
		box->addButton(rpl::single(u"Удалить всё"_q), [=] { box->closeBox(); remove(false); });
		box->addButton(tr::lng_cancel(), [=] { box->closeBox(); });
	}));
}

void SharePlugin(
		not_null<Window::SessionController*> controller,
		const QString &id,
		rpl::variable<QString> &notice) {
	const auto path = Request({
		{ u"action"_q, u"share_file"_q },
		{ u"installation_id"_q, id },
	}, notice).toString();
	if (!path.isEmpty()) {
		notice = QString();
		controller->content()->handleStartFiles({ path });
	}
}

class PluginDetails final : public AbstractSection {
public:
	PluginDetails(
		QWidget *parent,
		not_null<Window::SessionController*> controller,
		QString installationId,
		QString name);

	[[nodiscard]] Type id() const override;
	[[nodiscard]] rpl::producer<QString> title() override;
	[[nodiscard]] rpl::producer<> sectionShowBack() override;
	[[nodiscard]] static Type Id(QString installationId, QString name);

private:
	void refresh();
	void operate(const QString &action, bool keepData = false);
	void installUpdate();
	void addSettings(const QJsonArray &fields);
	void pollWhileInstalling(const QJsonObject &snapshot);

	const QString _installationId;
	const QString _name;
	const not_null<Ui::VerticalLayout*> _content;
	rpl::variable<QString> _notice;
	rpl::event_stream<> _back;
	bool _polling = false;
};

struct DetailsFactory final : AbstractSectionFactory {
	DetailsFactory(QString installationId, QString name)
	: installationId(std::move(installationId)), name(std::move(name)) {
	}

	object_ptr<AbstractSection> create(
			not_null<QWidget*> parent,
			not_null<Window::SessionController*> controller,
			not_null<Ui::ScrollArea*> scroll,
			rpl::producer<Container> containerValue) const override {
		return object_ptr<PluginDetails>(parent, controller, installationId, name);
	}

	const QString installationId;
	const QString name;
};

PluginDetails::PluginDetails(
	QWidget *parent,
	not_null<Window::SessionController*> controller,
	QString installationId,
	QString name)
: AbstractSection(parent, controller)
, _installationId(std::move(installationId))
, _name(std::move(name))
, _content(Ui::CreateChild<Ui::VerticalLayout>(this)) {
	setNavigationAnchor(_content);
	Ui::ResizeFitChild(this, _content);
	refresh();
}

Type PluginDetails::Id(QString installationId, QString name) {
	return std::make_shared<DetailsFactory>(std::move(installationId), std::move(name));
}

Type PluginDetails::id() const {
	return Id(_installationId, _name);
}

rpl::producer<QString> PluginDetails::title() {
	return rpl::single(_name);
}

rpl::producer<> PluginDetails::sectionShowBack() {
	return _back.events();
}

void PluginDetails::refresh() {
	const auto hold = HoldHeight(_content);
	Clear(_content);
	AddNotice(_content, _notice);
	const auto result = Request({ { u"action"_q, u"snapshot"_q } }, _notice);
	if (result.isUndefined()) {
		return;
	}
	const auto snapshot = result.toObject();
	const auto entries = snapshot.value(u"plugins"_q).toArray();
	auto plugin = QJsonObject();
	for (const auto &entry : entries) {
		const auto object = entry.toObject();
		if (object.value(u"installation_id"_q).toString() == _installationId) {
			plugin = object;
			break;
		}
	}
	if (plugin.isEmpty()) {
		_notice = u"Плагин удалён."_q;
		return;
	}

	const auto status = RuntimeStatus(snapshot);
	const auto enabled = plugin.value(u"enabled"_q).toBool();
	const auto card = AddCard(_content);
	AddPluginHeader(card, PluginStatus(plugin), nullptr, enabled,
		!status.isEmpty() || plugin.value(u"trust"_q).toObject().value(u"status"_q).toString() == u"blocked"_q, [=, this] {
			operate(enabled ? u"disable"_q : u"enable"_q);
		});
	AddTrustMetadata(card, plugin);
	AddCardLabel(card, plugin.value(u"description"_q).toString());
	if (const auto line = DependencyLine(plugin); !line.isEmpty()) {
		AddCardLabel(card, line, st::settingsPluginCardMeta);
	}
	if (const auto error = plugin.value(u"error"_q).toString(); !error.isEmpty()) {
		Ui::AddDividerText(_content, rpl::single(u"Ошибка: "_q + error));
	}
	if (!status.isEmpty()) {
		Ui::AddDividerText(_content, rpl::single(status));
	}
	if (const auto text = DependencyStatus(snapshot); !text.isEmpty()) {
		Ui::AddDividerText(_content, rpl::single(text));
	}
	pollWhileInstalling(snapshot);

	if (plugin.value(u"loaded"_q).toBool()) {
		const auto fields = Request({
			{ u"action"_q, u"settings"_q },
			{ u"installation_id"_q, _installationId },
		}, _notice);
		if (fields.isArray() && !fields.toArray().isEmpty()) {
			addSettings(fields.toArray());
		}
	}

	Ui::AddSkip(_content);
	Ui::AddDivider(_content);
	Ui::AddSkip(_content);
	Ui::AddSubsectionTitle(_content, rpl::single(u"Управление плагином"_q));
	AddAction(_content, u"Обновить из файла"_q, [this] { installUpdate(); });
	if (plugin.value(u"update"_q).isObject()) {
		const auto offer = plugin.value(u"update"_q).toObject();
		AddAction(_content, offer.value(u"rollback"_q).toBool()
			? u"Установить предыдущую безопасную версию"_q : u"Обновить из реестра"_q,
			[this] { operate(u"apply_update"_q); });
	}
	if (plugin.value(u"previous"_q).toBool()) {
		AddAction(_content, u"Откатить"_q, [this] { operate(u"rollback"_q); });
	}
	AddCardActions(
		AddCard(_content),
		[this] { SharePlugin(controller(), _installationId, _notice); },
		[this] {
			ConfirmRemove(controller(), crl::guard(this, [this](bool keepData) {
				operate(u"remove"_q, keepData);
			}));
		});
	Ui::AddSkip(_content);
}

void PluginDetails::pollWhileInstalling(const QJsonObject &snapshot) {
	if ((InstallingDependencies(snapshot) || snapshot.value(u"distribution"_q).toObject().value(u"busy"_q).toBool()) && !_polling) {
		_polling = true;
		QTimer::singleShot(kDependencyPoll, this, [this] {
			_polling = false;
			refresh();
		});
	}
}

void PluginDetails::operate(const QString &action, bool keepData) {
	const auto result = Request([&] {
		auto request = QJsonObject{ { u"action"_q, action }, { u"installation_id"_q, _installationId } };
		if (action == u"remove"_q) request.insert(u"keep_data"_q, keepData);
		return request;
	}(), _notice);
	const auto succeeded = !result.isUndefined();
	QTimer::singleShot(0, this, [=, this] {
		if (succeeded && action == u"remove"_q) {
			_back.fire({});
		} else {
			if (succeeded) {
				_notice = QString();
			}
			refresh();
		}
	});
}

void PluginDetails::installUpdate() {
	FileDialog::GetOpenPath(this, u"Выбрать файл плагина"_q, kPluginFilter,
		crl::guard(this, [this](const FileDialog::OpenResult &files) {
			if (!files.paths.isEmpty()) {
				Ovygram::ShowPluginInstall(files.paths.front(), _installationId,
					crl::guard(this, [this] { refresh(); }));
			}
		}));
}

void PluginDetails::addSettings(const QJsonArray &fields) {
	Ui::AddSkip(_content);
	Ui::AddDivider(_content);
	Ui::AddSkip(_content);
	Ui::AddSubsectionTitle(_content, rpl::single(u"Настройки плагина"_q));

	auto values = std::vector<std::pair<QString, Fn<QJsonValue()>>>();
	for (const auto &value : fields) {
		const auto field = value.toObject();
		const auto kind = field.value(u"kind"_q).toString();
		const auto text = field.value(u"text"_q).toString();
		const auto initial = field.value(u"value"_q);
		const auto key = field.value(u"key"_q).toString();
		if (kind == u"header"_q) {
			Ui::AddSubsectionTitle(_content, rpl::single(text));
		} else if (kind == u"button"_q) {
			AddAction(_content, text, [=, this] {
				(void)Request({ { u"action"_q, u"settings_action"_q },
					{ u"installation_id"_q, _installationId },
					{ u"action_id"_q, field.value(u"action_id"_q) } }, _notice);
				QTimer::singleShot(0, this, [this] { refresh(); });
			});
		} else if (kind == u"switch"_q) {
			const auto button = _content->add(object_ptr<Ui::SettingsButton>(
				_content,
				rpl::single(text),
				st::settingsButtonNoIcon
			))->toggleOn(rpl::single(initial.toBool()));
			values.emplace_back(key, [=] { return QJsonValue(button->toggled()); });
		} else if (kind == u"selector"_q) {
			Ui::AddSubsectionTitle(_content, rpl::single(text));
			const auto group = std::make_shared<Ui::RadiobuttonGroup>(initial.toInt());
			auto index = 0;
			for (const auto &item : field.value(u"items"_q).toArray()) {
				_content->add(
					object_ptr<Ui::Radiobutton>(
						_content,
						group,
						index++,
						item.toString(),
						st::settingsSendType),
					st::settingsSendTypePadding);
			}
			values.emplace_back(key, [=] { return QJsonValue(group->current()); });
		} else if (kind == u"input"_q) {
			Ui::AddSubsectionTitle(_content, rpl::single(text));
			const auto input = _content->add(
				object_ptr<Ui::InputField>(
					_content,
					st::defaultInputField,
					Ui::InputField::Mode::SingleLine,
					rpl::single(text),
					TextWithTags{ initial.toString() }),
				st::boxRowPadding);
			values.emplace_back(key, [=] { return QJsonValue(input->getLastText()); });
		}
	}
	AddAction(_content, u"Сохранить настройки"_q, [this, values = std::move(values)] {
		auto object = QJsonObject();
		for (const auto &[key, value] : values) {
			object.insert(key, value());
		}
		if (!Request({
			{ u"action"_q, u"save_settings"_q },
			{ u"installation_id"_q, _installationId },
			{ u"values"_q, object },
		}, _notice).isUndefined()) {
			_notice = u"Настройки сохранены."_q;
		}
	}, st::settingsButtonActive);
}

class Plugins final : public Section<Plugins> {
public:
	Plugins(QWidget *parent, not_null<Window::SessionController*> controller);

	[[nodiscard]] rpl::producer<QString> title() override;
	void showFinished() override;

private:
	void refresh();
	void populate();
	void install();
	void operate(const QString &id, const QString &action, bool keepData = false);

	std::unique_ptr<Ui::SearchFieldController> _search;
	Ui::VerticalLayout *_content = nullptr;
	QJsonObject _snapshot;
	QString _query;
	rpl::variable<QString> _notice;
	bool _polling = false;
};

Plugins::Plugins(
	QWidget *parent,
	not_null<Window::SessionController*> controller)
: Section(parent, controller) {
	const auto layout = Ui::CreateChild<Ui::VerticalLayout>(this);
	auto search = CreateSectionSearchRow(layout);
	_search = std::move(search.controller);
	layout->add(object_ptr<Ui::RpWidget>::fromRaw(search.row.get()));
	setNavigationAnchor(layout);
	AddNotice(layout, _notice);
	AddAction(layout, u"Импортировать плагин"_q, [this] { install(); }, st::settingsPluginImport);
	AddAction(layout, u"Проверить обновления"_q, [this] {
		(void)Request({ { u"action"_q, u"check_updates"_q } }, _notice);
		refresh();
	});
	_content = layout->add(object_ptr<Ui::VerticalLayout>(layout));
	Ui::ResizeFitChild(this, layout);

	_search->queryChanges() | rpl::on_next([this](const QString &query) {
		_query = query.trimmed();
		populate();
	}, layout->lifetime());
	refresh();
}

rpl::producer<QString> Plugins::title() {
	return rpl::single(u"Плагины"_q);
}

void Plugins::showFinished() {
	Section<Plugins>::showFinished();
	refresh();
}

void Plugins::refresh() {
	_snapshot = Request({ { u"action"_q, u"snapshot"_q } }, _notice).toObject();
	populate();
	// The plugin starts when its libraries are installed in the background.
	if ((InstallingDependencies(_snapshot) || _snapshot.value(u"distribution"_q).toObject().value(u"busy"_q).toBool()) && !_polling) {
		_polling = true;
		QTimer::singleShot(kDependencyPoll, this, [this] {
			_polling = false;
			refresh();
		});
	}
}

void Plugins::populate() {
	const auto hold = HoldHeight(_content);
	Clear(_content);
	if (_snapshot.isEmpty()) {
		return;
	}
	for (const auto &notice : _snapshot.value(u"distribution"_q).toObject().value(u"notices"_q).toArray()) {
		Ui::AddDividerText(_content, rpl::single(notice.toString()));
	}
	const auto status = RuntimeStatus(_snapshot);
	if (!status.isEmpty()) {
		Ui::AddDividerText(_content, rpl::single(status));
	}
	if (const auto text = DependencyStatus(_snapshot); !text.isEmpty()) {
		Ui::AddDividerText(_content, rpl::single(text));
	}
	if (_snapshot.value(u"recovery"_q).toBool()
		&& !_snapshot.value(u"disabled"_q).toBool()
		&& !_snapshot.value(u"restart_required"_q).toBool()) {
		AddAction(_content, u"Возобновить запуск плагинов"_q, [this] {
			_notice = QString();
			(void)Request({ { u"action"_q, u"resume"_q } }, _notice);
			crl::on_main(this, [this] { refresh(); });
		});
	}
	Ui::AddSkip(_content);
	Ui::AddDivider(_content);
	Ui::AddSkip(_content);
	Ui::AddSubsectionTitle(_content, rpl::single(u"Установленные плагины"_q));
	const auto entries = _snapshot.value(u"plugins"_q).toArray();
	auto found = false;
	for (const auto &entry : entries) {
		const auto plugin = entry.toObject();
		const auto name = plugin.value(u"name"_q).toString();
		const auto id = plugin.value(u"installation_id"_q).toString();
		const auto pluginId = plugin.value(u"plugin_id"_q).toString();
		const auto author = plugin.value(u"author"_q).toString();
		if (!name.contains(_query, Qt::CaseInsensitive)
			&& !pluginId.contains(_query, Qt::CaseInsensitive)
			&& !author.contains(_query, Qt::CaseInsensitive)) {
			continue;
		}
		found = true;
		const auto card = AddCard(_content);
		const auto enabled = plugin.value(u"enabled"_q).toBool();
		AddPluginHeader(
			card, name,
			[=, this] { showOther(PluginDetails::Id(id, name)); },
			enabled, !status.isEmpty() || plugin.value(u"trust"_q).toObject().value(u"status"_q).toString() == u"blocked"_q,
			[=, this] { operate(id, enabled ? u"disable"_q : u"enable"_q); });
		AddTrustMetadata(card, plugin);
		AddCardLabel(card, DescriptionPreview(plugin.value(u"description"_q).toString()));
		if (const auto line = DependencyLine(plugin); !line.isEmpty()) {
			AddCardLabel(card, line, st::settingsPluginCardMeta);
		}
		if (const auto error = plugin.value(u"error"_q).toString(); !error.isEmpty()) {
			AddCardLabel(card, u"Ошибка: "_q + DescriptionPreview(error), st::settingsPluginCardMeta);
		}
		AddCardActions(
			card,
			[=, this] { SharePlugin(controller(), id, _notice); },
			[=, this] {
				ConfirmRemove(controller(), crl::guard(this, [=, this](bool keepData) {
					operate(id, u"remove"_q, keepData);
				}));
			});
	}
	if (!found) {
		Ui::AddDividerText(_content, rpl::single(entries.isEmpty()
			? u"Установленных плагинов пока нет."_q
			: u"Плагины не найдены."_q));
	}
	Ui::AddSkip(_content);
	Ui::AddDivider(_content);
	AddAction(_content, u"Открыть журнал"_q, [this] {
		const auto path = _snapshot.value(u"log_path"_q).toString();
		if (path.isEmpty() || !QDesktopServices::openUrl(QUrl::fromLocalFile(path))) {
			_notice = u"Не удалось открыть журнал плагинов."_q;
		}
	});
	Ui::AddSkip(_content);
}

void Plugins::operate(const QString &id, const QString &action, bool keepData) {
	_notice = QString();
	(void)Request([&] {
		auto request = QJsonObject{ { u"action"_q, action }, { u"installation_id"_q, id } };
		if (action == u"remove"_q) request.insert(u"keep_data"_q, keepData);
		return request;
	}(), _notice);
	QTimer::singleShot(0, this, [this] { refresh(); });
}

void Plugins::install() {
	FileDialog::GetOpenPath(this, u"Выбрать файл плагина"_q, kPluginFilter,
		crl::guard(this, [this](const FileDialog::OpenResult &files) {
			if (!files.paths.isEmpty()) {
				Ovygram::ShowPluginInstall(files.paths.front(), QString(),
					crl::guard(this, [this] { refresh(); }));
			}
		}));
}

} // namespace

Type PluginsId() {
	return Plugins::Id();
}

} // namespace Settings
