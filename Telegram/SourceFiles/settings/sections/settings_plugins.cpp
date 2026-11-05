#include "settings/sections/settings_plugins.h"

#include "core/application.h"
#include "core/file_utilities.h"
#include "core/plugin_runtime.h"
#include "lang/lang_keys.h"
#include "settings/settings_common_session.h"
#include "ui/boxes/confirm_box.h"
#include "ui/search_field_controller.h"
#include "ui/vertical_list.h"
#include "ui/widgets/buttons.h"
#include "ui/widgets/checkbox.h"
#include "ui/widgets/fields/input_field.h"
#include "ui/wrap/vertical_layout.h"
#include "window/window_session_controller.h"
#include "styles/style_layers.h"
#include "styles/style_settings.h"

#include <QtCore/QJsonArray>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonObject>
#include <QtCore/QUrl>
#include <QtGui/QDesktopServices>

namespace Settings {
namespace {

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

class PluginDetails final : public AbstractSection {
public:
	PluginDetails(
		QWidget *parent,
		not_null<Window::SessionController*> controller,
		QString pluginId,
		QString name);

	[[nodiscard]] Type id() const override;
	[[nodiscard]] rpl::producer<QString> title() override;
	[[nodiscard]] rpl::producer<> sectionShowBack() override;
	[[nodiscard]] static Type Id(QString pluginId, QString name);

private:
	void refresh();
	void operate(const QString &action);
	void installUpdate();
	void addSettings(const QJsonArray &fields);

	const QString _pluginId;
	const QString _name;
	const not_null<Ui::VerticalLayout*> _content;
	rpl::variable<QString> _notice;
	rpl::event_stream<> _back;
};

struct DetailsFactory final : AbstractSectionFactory {
	DetailsFactory(QString pluginId, QString name)
	: pluginId(std::move(pluginId)), name(std::move(name)) {
	}

	object_ptr<AbstractSection> create(
			not_null<QWidget*> parent,
			not_null<Window::SessionController*> controller,
			not_null<Ui::ScrollArea*> scroll,
			rpl::producer<Container> containerValue) const override {
		return object_ptr<PluginDetails>(parent, controller, pluginId, name);
	}

	const QString pluginId;
	const QString name;
};

PluginDetails::PluginDetails(
	QWidget *parent,
	not_null<Window::SessionController*> controller,
	QString pluginId,
	QString name)
: AbstractSection(parent, controller)
, _pluginId(std::move(pluginId))
, _name(std::move(name))
, _content(Ui::CreateChild<Ui::VerticalLayout>(this)) {
	setNavigationAnchor(_content);
	Ui::ResizeFitChild(this, _content);
	refresh();
}

Type PluginDetails::Id(QString pluginId, QString name) {
	return std::make_shared<DetailsFactory>(std::move(pluginId), std::move(name));
}

Type PluginDetails::id() const {
	return Id(_pluginId, _name);
}

rpl::producer<QString> PluginDetails::title() {
	return rpl::single(_name);
}

rpl::producer<> PluginDetails::sectionShowBack() {
	return _back.events();
}

void PluginDetails::refresh() {
	Clear(_content);
	Ui::AddDividerText(_content, _notice.value());
	const auto result = Request({ { u"action"_q, u"snapshot"_q } }, _notice);
	if (result.isUndefined()) {
		return;
	}
	const auto snapshot = result.toObject();
	const auto entries = snapshot.value(u"plugins"_q).toArray();
	auto plugin = QJsonObject();
	for (const auto &entry : entries) {
		const auto object = entry.toObject();
		if (object.value(u"id"_q).toString() == _pluginId) {
			plugin = object;
			break;
		}
	}
	if (plugin.isEmpty()) {
		_notice = u"Плагин удалён."_q;
		return;
	}

	auto about = _pluginId + u" · "_q + plugin.value(u"version"_q).toString()
		+ u" · "_q + plugin.value(u"author"_q).toString() + u"\n"_q
		+ PluginStatus(plugin) + u"\n\n"_q
		+ plugin.value(u"description"_q).toString();
	if (const auto error = plugin.value(u"error"_q).toString(); !error.isEmpty()) {
		about += u"\n\nОшибка: "_q + error;
	}
	Ui::AddDividerText(_content, rpl::single(std::move(about)));
	const auto status = RuntimeStatus(snapshot);
	if (!status.isEmpty()) {
		Ui::AddDividerText(_content, rpl::single(status));
	}
	const auto enabled = plugin.value(u"enabled"_q).toBool();
	if (enabled || status.isEmpty()) {
		AddAction(
			_content,
			enabled ? u"Отключить"_q : u"Включить"_q,
			[=, this] { operate(enabled ? u"disable"_q : u"enable"_q); });
	}

	if (plugin.value(u"loaded"_q).toBool()) {
		const auto fields = Request({
			{ u"action"_q, u"settings"_q },
			{ u"plugin_id"_q, _pluginId },
		}, _notice);
		if (fields.isArray() && !fields.toArray().isEmpty()) {
			addSettings(fields.toArray());
		}
	}

	Ui::AddSkip(_content);
	Ui::AddDivider(_content);
	AddAction(_content, u"Обновить из файла"_q, [this] { installUpdate(); });
	if (plugin.value(u"previous"_q).toBool()) {
		AddAction(_content, u"Откатить"_q, [this] { operate(u"rollback"_q); });
	}
	AddAction(_content, u"Удалить"_q, [this] {
		controller()->show(Ui::MakeConfirmBox({
			.text = rpl::single(u"Удалить этот плагин и его настройки?"_q),
			.confirmed = crl::guard(this, [this] { operate(u"remove"_q); }),
			.confirmText = tr::lng_box_delete(),
			.confirmStyle = &st::attentionBoxButton,
		}));
	});
	Ui::AddSkip(_content);
}

void PluginDetails::operate(const QString &action) {
	const auto result = Request({
		{ u"action"_q, action },
		{ u"plugin_id"_q, _pluginId },
	}, _notice);
	const auto succeeded = !result.isUndefined();
	crl::on_main(this, [=, this] {
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
	FileDialog::GetOpenPath(
		this,
		u"Выбрать файл плагина"_q,
		u"Плагины (*.py *.plugin *.zip)"_q,
		crl::guard(this, [this](const FileDialog::OpenResult &files) {
			if (!files.paths.isEmpty() && !Request({
				{ u"action"_q, u"install"_q },
				{ u"path"_q, files.paths.front() },
				{ u"plugin_id"_q, _pluginId },
			}, _notice).isUndefined()) {
				_notice = QString();
				refresh();
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
		if (kind == u"switch"_q) {
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
			{ u"plugin_id"_q, _pluginId },
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

private:
	void refresh();
	void populate();
	void install();

	std::unique_ptr<Ui::SearchFieldController> _search;
	Ui::VerticalLayout *_content = nullptr;
	QJsonObject _snapshot;
	QString _query;
	rpl::variable<QString> _notice;
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
	Ui::AddDividerText(layout, _notice.value());
	AddAction(layout, u"Импорт"_q, [this] { install(); }, st::settingsButtonActive);
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

void Plugins::refresh() {
	_snapshot = Request({ { u"action"_q, u"snapshot"_q } }, _notice).toObject();
	populate();
}

void Plugins::populate() {
	Clear(_content);
	if (_snapshot.isEmpty()) {
		return;
	}
	const auto status = RuntimeStatus(_snapshot);
	if (!status.isEmpty()) {
		Ui::AddDividerText(_content, rpl::single(status));
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
		const auto id = plugin.value(u"id"_q).toString();
		if (!name.contains(_query, Qt::CaseInsensitive)
			&& !id.contains(_query, Qt::CaseInsensitive)) {
			continue;
		}
		found = true;
		AddButtonWithLabel(
			_content,
			rpl::single(name),
			rpl::single(PluginStatus(plugin)),
			st::settingsButtonNoIcon
		)->setClickedCallback([=, this] { showOther(PluginDetails::Id(id, name)); });
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

void Plugins::install() {
	FileDialog::GetOpenPath(
		this,
		u"Выбрать файл плагина"_q,
		u"Плагины (*.py *.plugin *.zip)"_q,
		crl::guard(this, [this](const FileDialog::OpenResult &files) {
			if (!files.paths.isEmpty() && !Request({
				{ u"action"_q, u"install"_q },
				{ u"path"_q, files.paths.front() },
			}, _notice).isUndefined()) {
				_notice = u"Плагин импортирован. Он выключен."_q;
				refresh();
			}
		}));
}

} // namespace

Type PluginsId() {
	return Plugins::Id();
}

} // namespace Settings
