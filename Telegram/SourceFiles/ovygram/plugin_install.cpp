#include "ovygram/plugin_install.h"

#include "core/application.h"
#include "core/plugin_runtime.h"

#include <QtCore/QJsonArray>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonObject>
#include <QtCore/QTimer>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QDialogButtonBox>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QVBoxLayout>

#include <stdexcept>

namespace Ovygram {
namespace {

int ActiveInstallers = 0;

QJsonValue Request(const QJsonObject &request) {
	const auto runtime = Core::App().pluginRuntime();
	if (!runtime) {
		throw std::runtime_error("Встроенный Python недоступен.");
	}
	const auto response = QJsonDocument::fromJson(QByteArray::fromStdString(
		runtime->dispatch(QJsonDocument(request).toJson(QJsonDocument::Compact).toStdString()))).object();
	if (!response.contains(u"result"_q)) {
		throw std::runtime_error(response.value(u"error"_q).toString().toStdString());
	}
	return response.value(u"result"_q);
}

bool Trusted(const QString &status) {
	return status == u"verified"_q || status == u"official"_q;
}

QString StatusText(const QString &status) {
	if (status == u"official"_q) return u"Официальный плагин"_q;
	if (status == u"verified"_q) return u"Проверенный плагин"_q;
	if (status == u"blocked"_q) return u"Опасный плагин / вирус. Установка запрещена."_q;
	if (status == u"revoked"_q) return u"Непроверенный плагин — проверка отозвана"_q;
	if (status == u"verification_unavailable"_q) return u"Сервер не отвечает — невозможно проверить плагин"_q;
	return u"Непроверенный плагин"_q;
}

// All labels use PlainText, including metadata. No plugin-created widgets,
// handles, callbacks, rich text links or system badges enter this dialog.
class InstallDialog final : public QDialog {
public:
	InstallDialog(QString path, QString installationId, Fn<void()> done)
	: QDialog(nullptr)
	, _installationId(std::move(installationId))
	, _done(std::move(done)) {
		++ActiveInstallers;
		setAttribute(Qt::WA_DeleteOnClose);
		setWindowModality(Qt::ApplicationModal);
		setWindowTitle(u"Установка плагина Ovygram"_q);
		resize(580, 580);
			if (const auto window = QApplication::activeWindow()) {
				move(window->frameGeometry().center() - rect().center());
			}
		const auto layout = new QVBoxLayout(this);
		const auto scroll = new QScrollArea(this);
		scroll->setWidgetResizable(true);
		const auto content = new QWidget(scroll);
		_rows = new QVBoxLayout(content);
		_rows->setAlignment(Qt::AlignTop);
		_rows->setSizeConstraint(QLayout::SetMinAndMaxSize);
		scroll->setWidget(content);
		layout->addWidget(scroll);
		_buttons = new QDialogButtonBox(this);
		layout->addWidget(_buttons);
		label(u"Чтение метаданных и проверка файла…"_q);
		cancel();
		_timer = new QTimer(this);
		connect(_timer, &QTimer::timeout, this, [this] { poll(); });
		try {
			_token = Request({ { u"action"_q, u"prepare_install"_q }, { u"path"_q, path } }).toString();
			_timer->start(200);
		} catch (const std::exception &error) {
			label(QString::fromUtf8(error.what()), u"#b00020"_q);
		}
	}

	~InstallDialog() {
		if (!_token.isEmpty()) {
			try {
				(void)Request({ { u"action"_q, u"discard_install"_q }, { u"token"_q, _token } });
			} catch (...) {
			}
		}
		--ActiveInstallers;
		if (_done) _done();
	}

private:
	void label(QString text, QString color = QString()) {
		const auto value = new QLabel(std::move(text), this);
		value->setTextFormat(Qt::PlainText);
		value->setWordWrap(true);
		value->setTextInteractionFlags(Qt::TextSelectableByMouse);
		if (!color.isEmpty()) value->setStyleSheet(u"color: %1"_q.arg(color));
		_rows->addWidget(value);
	}

	void cancel() {
		const auto button = _buttons->addButton(u"Отмена"_q, QDialogButtonBox::RejectRole);
		button->setDefault(true);
		connect(button, &QPushButton::clicked, this, [this] { reject(); });
	}

	void action(QString text, Fn<void()> callback) {
		const auto button = _buttons->addButton(std::move(text), QDialogButtonBox::ActionRole);
		button->setAutoDefault(false);
		connect(button, &QPushButton::clicked, this, [callback = std::move(callback)] {
			// The callback may replace the buttons, deleting this connection.
			const auto invoke = callback;
			invoke();
		});
	}

	void poll() {
		try {
			const auto info = Request({ { u"action"_q, u"prepared_install"_q }, { u"token"_q, _token } }).toObject();
			const auto state = info.value(u"state"_q).toString();
			if (state == u"pending"_q) return;
			_timer->stop();
			if (state != u"ready"_q) {
				label(info.value(u"error"_q).toString(), u"#b00020"_q);
				return;
			}
			_info = info;
			const auto progress = _rows->takeAt(0);
			delete progress->widget();
			delete progress;
			showChoices();
		} catch (const std::exception &error) {
			_timer->stop();
			label(QString::fromUtf8(error.what()), u"#b00020"_q);
		}
	}

	void details(const QJsonObject &metadata, const QJsonObject &trust) {
		label(u"%1 · %2\n%3"_q.arg(metadata.value(u"name"_q).toString(),
			metadata.value(u"version"_q).toString(), metadata.value(u"description"_q).toString()));
		label(u"Автор: "_q + metadata.value(u"display_author"_q).toString(metadata.value(u"author"_q).toString()),
			metadata.value(u"author_hidden"_q).toBool() ? u"#b00020"_q : QString());
		const auto status = trust.value(u"status"_q).toString();
		label(StatusText(status), status == u"official"_q ? u"#1565c0"_q
			: status == u"verified"_q ? u"#188038"_q : u"#b00020"_q);
	}

	void showChoices() {
		const auto metadata = _info.value(u"metadata"_q).toObject();
		const auto trust = _info.value(u"trust"_q).toObject();
		const auto status = trust.value(u"status"_q).toString();
		details(metadata, trust);
		label(u"ID: "_q + metadata.value(u"id"_q).toString());
			label(metadata.value(u"release"_q).toBool()
				? u"Публичная версия — доступна для механизма обновлений"_q
				: u"Непубличная версия — автоматический поиск обновлений отключён"_q);
		label(u"SHA-256: "_q + _info.value(u"sha256"_q).toString());
		if (status == u"blocked"_q) return;
		const auto installations = _info.value(u"installations"_q).toArray();
		auto hasTrusted = false;
		for (const auto &value : installations) {
			const auto old = value.toObject();
			const auto id = old.value(u"installation_id"_q).toString();
			label(u"Установленный экземпляр "_q + id.left(8));
			details(old, old.value(u"trust"_q).toObject());
			hasTrusted = hasTrusted || Trusted(old.value(u"trust"_q).toObject().value(u"status"_q).toString());
			if (_installationId.isEmpty() || _installationId == id) {
				action(u"Обновить "_q + id.left(8), [=, this] { confirm(id, false, old); });
			}
		}
		if (!_installationId.isEmpty() && installations.isEmpty()) {
			label(u"ID файла не совпадает с ID обновляемого экземпляра."_q, u"#b00020"_q);
			return;
		}
		if (_installationId.isEmpty() && (!hasTrusted || !Trusted(status))) {
			action(installations.isEmpty() ? u"Установить"_q : u"Установить отдельно"_q,
				[=, this] { confirm(QString(), !installations.isEmpty(), QJsonObject()); });
		}
	}

	void confirm(QString id, bool separate, QJsonObject old) {
		const auto status = _info.value(u"trust"_q).toObject().value(u"status"_q).toString();
		const auto loss = (old.value(u"previously_trusted"_q).toBool()
			|| Trusted(old.value(u"trust"_q).toObject().value(u"status"_q).toString())) && !Trusted(status);
		const auto unavailable = status == u"verification_unavailable"_q;
		if ((loss || unavailable) && !_warned) {
			_buttons->clear();
			cancel();
			if (loss) label(u"Вы заменяете проверенный плагин непроверенной версией. Автор и безопасность "
				"нового файла не подтверждены. Плагин потеряет статус проверки. Рекомендуется отменить "
				"замену либо установить файл отдельно."_q, u"#b00020"_q);
			if (unavailable) label(u"Сервер не ответил. Невозможно проверить, заблокирован ли этот файл. "
				"Продолжайте только если доверяете источнику."_q, u"#b00020"_q);
			_warned = true;
			action(u"Подтверждаю установку"_q, [=, this] { confirm(id, separate, old); });
			return;
		}
		try {
			(void)Request({ { u"action"_q, u"commit_install"_q }, { u"token"_q, _token },
				{ u"installation_id"_q, id }, { u"separate"_q, separate },
				{ u"allow_unavailable"_q, unavailable && _warned }, { u"allow_loss"_q, loss && _warned } });
			_token.clear();
			accept();
		} catch (const std::exception &error) {
			label(QString::fromUtf8(error.what()), u"#b00020"_q);
		}
	}

	QString _token;
	QString _installationId;
	Fn<void()> _done;
	QJsonObject _info;
	QVBoxLayout *_rows = nullptr;
	QDialogButtonBox *_buttons = nullptr;
	QTimer *_timer = nullptr;
	bool _warned = false;
};

} // namespace

bool InstallationUiActive() {
	return ActiveInstallers != 0;
}

void ShowPluginInstall(const QString &path, const QString &installationId, Fn<void()> done) {
	if (InstallationUiActive()) return;
	(new InstallDialog(path, installationId, std::move(done)))->show();
}

} // namespace Ovygram
