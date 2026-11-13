#include "ovygram/plugin_install.h"
#include "core/application.h"
#include "core/plugin_runtime.h"

#include <QtCore/QJsonArray>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonObject>
#include <QtCore/QTimer>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>

#include <iostream>

namespace {
int Commits = 0;
bool Success = false;
QString Mode;
QString Screenshot;
}

namespace Core {
Application &App() {
	static Application application;
	return application;
}
PluginRuntime *Application::pluginRuntime() {
	// dispatch() below has no member accesses. This fixture never constructs
	// Python; protocol and actual embedded-host tests run separately.
	static auto runtime = PluginRuntime({}, {}, true);
	return &runtime;
}
struct PluginRuntime::Private {};
PluginRuntime::PluginRuntime(const std::filesystem::path &, const std::filesystem::path &, bool)
: _private(std::make_unique<Private>()) {
}
PluginRuntime::~PluginRuntime() = default;
std::string PluginRuntime::dispatch(const std::string &request) {
	const auto command = QJsonDocument::fromJson(QByteArray::fromStdString(request)).object();
	const auto action = command.value(u"action"_q).toString();
	auto result = QJsonValue();
	if (action == u"prepare_install"_q) {
		result = u"test-token"_q;
	} else if (action == u"prepared_install"_q) {
		const auto metadata = QJsonObject{
			{u"id"_q, u"test_plugin"_q}, {u"name"_q, u"<b>Plugin name is plain text</b>"_q},
			{u"version"_q, u"1.2"_q}, {u"description"_q, u"Full description\nSecond line"_q},
			{u"author"_q, u"Ovygram"_q}, {u"display_author"_q, u"Неизвестный автор"_q},
			{u"author_hidden"_q, true}};
		const auto status = Mode == u"blocked"_q ? u"blocked"_q
			: Mode == u"offline"_q ? u"verification_unavailable"_q
			: Mode == u"verified"_q ? u"verified"_q : u"unverified"_q;
		auto installations = QJsonArray();
		if (Mode == u"loss"_q || Mode == u"verified"_q) {
			installations.push_back(QJsonObject{{u"installation_id"_q, u"12345678"_q},
				{u"name"_q, u"Installed version"_q}, {u"version"_q, u"1.1"_q},
				{u"description"_q, u"Old full description"_q}, {u"author"_q, u"Verified author"_q},
				{u"trust"_q, QJsonObject{{u"status"_q, u"verified"_q}}}});
		}
		result = QJsonObject{{u"state"_q, u"ready"_q}, {u"metadata"_q, metadata},
			{u"trust"_q, QJsonObject{{u"status"_q, status}}}, {u"sha256"_q, QString(64, QChar('a'))},
			{u"installations"_q, installations}};
	} else if (action == u"commit_install"_q) {
		if ((Mode == u"offline"_q && !command.value(u"allow_unavailable"_q).toBool())
			|| (Mode == u"loss"_q && !command.value(u"installation_id"_q).toString().isEmpty()
				&& !command.value(u"allow_loss"_q).toBool()) || Mode == u"blocked"_q) {
			return R"({"error":"missing confirmation"})";
		}
		++Commits;
		result = u"new-installation"_q;
	}
	return QJsonDocument(QJsonObject{{u"result"_q, result}}).toJson().toStdString();
}
} // namespace Core

int main(int argc, char **argv) {
	auto app = QApplication(argc, argv);
	if (argc < 2) return 2;
	Mode = QString::fromUtf8(argv[1]);
	Screenshot = argc > 2 ? QString::fromUtf8(argv[2]) : QString();
	Ovygram::ShowPluginInstall(u"fixture.ovyplugin"_q, QString(), [&] { app.quit(); });
	auto timer = QTimer();
	auto step = 0;
	QObject::connect(&timer, &QTimer::timeout, [&] {
		QDialog *dialog = nullptr;
		for (const auto widget : app.topLevelWidgets()) {
			if ((dialog = qobject_cast<QDialog*>(widget)) && dialog->isVisible()) break;
			dialog = nullptr;
		}
		if (!dialog) return;
		const auto labels = dialog->findChildren<QLabel*>();
		for (auto i = 0; i < labels.size(); ++i) {
			if (labels[i]->textFormat() != Qt::PlainText || labels[i]->height() <= 0) app.exit(9);
			for (auto j = i + 1; j < labels.size(); ++j) {
				if (labels[i]->parentWidget() == labels[j]->parentWidget()
					&& labels[i]->geometry().intersects(labels[j]->geometry())) app.exit(10);
			}
		}
		const auto buttons = dialog->findChildren<QPushButton*>();
		QPushButton *action = nullptr;
		QPushButton *cancel = nullptr;
		for (const auto button : buttons) {
			if (button->text() == u"Отмена"_q) cancel = button;
			else action = button;
			if (button->text() == u"Установить отдельно"_q && Mode == u"verified"_q) app.exit(3);
		}
		if (Mode == u"loss"_q && step == 0) {
			for (const auto button : buttons) {
				if (button->text().startsWith(u"Обновить "_q)) action = button;
			}
		}
		if (!cancel || !cancel->isDefault() || !Ovygram::InstallationUiActive()) app.exit(4);
		if (Mode == u"blocked"_q) {
			if (buttons.size() != 1) app.exit(5);
			if (++step < 4) return; // Wait for async preparation.
			Success = Commits == 0;
			if (!Screenshot.isEmpty()) dialog->grab().save(Screenshot);
			cancel->click();
		} else if (action) {
			if (!Screenshot.isEmpty()) dialog->grab().save(Screenshot);
			if (step == 0 && Commits != 0) app.exit(6);
			++step;
			action->click();
			if (step == 1 && (Mode == u"loss"_q || Mode == u"offline"_q) && Commits != 0) app.exit(6);
			Success = Commits == 1;
		}
	});
	timer.start(250);
	QTimer::singleShot(5000, [&] { app.exit(7); });
	const auto result = app.exec();
	if (result || !Success) return result ? result : 8;
	std::cout << Mode.toStdString() << ": passed\n";
	return 0;
}
