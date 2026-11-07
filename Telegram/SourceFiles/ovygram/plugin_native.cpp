#include "ovygram/plugin_native.h"

#include "ovygram/plugin_widgets.h"

#include <QtCore/QJsonArray>
#include <QtCore/QMetaMethod>
#include <QtCore/QMetaObject>
#include <QtCore/QPointer>
#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QWidget>

#include <array>
#include <map>
#include <memory>
#include <stdexcept>

namespace Ovygram::Native {
namespace {

constexpr auto kMaximumArguments = 10;

// Receives any signal: connected to a slot index this class doesn't
// declare, so every emission arrives in qt_metacall().
class SignalRelay final : public QObject {
public:
	SignalRelay(
		not_null<QObject*> source,
		QMetaMethod signal,
		std::function<void(QJsonArray)> callback)
	: QObject(source)
	, _signal(signal)
	, _callback(std::move(callback)) {
		const auto slot = QObject::staticMetaObject.methodCount();
		if (!QMetaObject::connect(
				source,
				signal.methodIndex(),
				this,
				slot,
				Qt::DirectConnection)) {
			throw std::runtime_error("The signal can't be connected.");
		}
	}

	int qt_metacall(QMetaObject::Call call, int id, void **arguments) override {
		id = QObject::qt_metacall(call, id, arguments);
		if (id < 0 || call != QMetaObject::InvokeMetaMethod) {
			return id;
		} else if (id == 0) {
			auto values = QJsonArray();
			for (auto i = 0; i != _signal.parameterCount(); ++i) {
				const auto type = _signal.parameterMetaType(i);
				values.push_back(type.isValid()
					? Widgets::VariantToJson(QVariant(type, arguments[i + 1]))
					: QJsonValue());
			}
			_callback(std::move(values));
		}
		return -1;
	}

private:
	const QMetaMethod _signal;
	const std::function<void(QJsonArray)> _callback;

};

class WindowFilter final : public QObject {
protected:
	bool eventFilter(QObject *watched, QEvent *e) override;
};

struct Connection {
	QString pluginId;
	QPointer<SignalRelay> relay;
};

struct State {
	std::function<void(QJsonObject)> send;
	std::map<QString, QString> windowWatchers; // Rule ID -> plugin ID.
	std::map<QString, Connection> connections; // Rule ID -> connection.
	std::unique_ptr<WindowFilter> filter;
};

State &Get() {
	// Leaked on purpose, like the other filters: it must outlive widgets.
	static const auto result = new State();
	return *result;
}

[[nodiscard]] QString WindowKind(not_null<QWidget*> widget) {
	switch (widget->windowType()) {
	case Qt::Popup: return u"popup"_q;
	case Qt::Dialog:
	case Qt::Sheet: return u"dialog"_q;
	case Qt::Window: return u"window"_q;
	default: return u"other"_q;
	}
}

bool WindowFilter::eventFilter(QObject *watched, QEvent *e) {
	const auto type = e->type();
	if (type != QEvent::Show && type != QEvent::Hide) {
		return false;
	}
	const auto widget = qobject_cast<QWidget*>(watched);
	if (!widget
		|| !widget->isWindow()
		|| widget->windowType() == Qt::ToolTip) {
		return false;
	}
	const auto &state = Get();
	if (state.windowWatchers.empty() || !state.send) {
		return false;
	}
	const auto value = QJsonObject{
		{ u"event"_q, (type == QEvent::Show) ? u"shown"_q : u"hidden"_q },
		{ u"handle"_q, Widgets::HandleFor(widget) },
		{ u"cls"_q, Widgets::ClassNameOf(widget) },
		{ u"kind"_q, WindowKind(widget) },
		{ u"title"_q, widget->windowTitle() },
	};
	const auto watchers = state.windowWatchers;
	for (const auto &[ruleId, pluginId] : watchers) {
		state.send(QJsonObject{
			{ u"plugin_id"_q, pluginId },
			{ u"type"_q, u"native_window"_q },
			{ u"rule_id"_q, ruleId },
			{ u"value"_q, value },
		});
	}
	return false;
}

[[nodiscard]] QWidget *Required(const QJsonValue &handle) {
	const auto result = Widgets::Resolve(handle);
	if (!result) {
		throw std::runtime_error("The widget no longer exists.");
	}
	return result;
}

[[nodiscard]] QString MethodType(const QMetaMethod &method) {
	switch (method.methodType()) {
	case QMetaMethod::Signal: return u"signal"_q;
	case QMetaMethod::Slot: return u"slot"_q;
	case QMetaMethod::Method: return u"method"_q;
	case QMetaMethod::Constructor: return u"constructor"_q;
	}
	return QString();
}

// A signal by its name or full signature, e.g. "clicked" or "clicked(bool)".
[[nodiscard]] QMetaMethod FindSignal(
		not_null<const QMetaObject*> meta,
		const QString &name) {
	const auto wanted = name.toLatin1();
	auto found = QMetaMethod();
	for (auto i = 0; i != meta->methodCount(); ++i) {
		const auto method = meta->method(i);
		if (method.methodType() != QMetaMethod::Signal) {
			continue;
		} else if (method.methodSignature() == wanted) {
			return method;
		} else if (method.name() == wanted && !found.isValid()) {
			found = method;
		}
	}
	if (!found.isValid()) {
		throw std::runtime_error("Unknown signal: " + name.toStdString());
	}
	return found;
}

QJsonValue Invoke(not_null<QWidget*> widget, const QJsonObject &command) {
	const auto name = command.value(u"name"_q).toString().toLatin1();
	const auto args = command.value(u"args"_q).toArray();
	if (args.size() > kMaximumArguments) {
		throw std::runtime_error("Too many arguments.");
	}
	const auto meta = widget->metaObject();
	auto lastError = std::string("Unknown method or wrong argument count.");
	for (auto i = 0; i != meta->methodCount(); ++i) {
		const auto method = meta->method(i);
		if (method.name() != name
			|| method.parameterCount() != args.size()
			|| method.access() != QMetaMethod::Public
			|| (method.methodType() != QMetaMethod::Slot
				&& method.methodType() != QMetaMethod::Method)) {
			continue;
		}
		auto values = std::array<QVariant, kMaximumArguments>();
		auto arguments = std::array<QGenericArgument, kMaximumArguments>();
		try {
			for (auto k = 0; k != args.size(); ++k) {
				const auto type = method.parameterMetaType(k);
				values[k] = Widgets::JsonToVariant(args[k], type.id());
				arguments[k] = QGenericArgument(type.name(), values[k].constData());
			}
		} catch (const std::exception &error) {
			lastError = error.what(); // Try an overload with other types.
			continue;
		}
		const auto returnType = method.returnMetaType();
		const auto returns = returnType.isValid()
			&& returnType.id() != QMetaType::Void;
		auto result = returns ? QVariant(returnType) : QVariant();
		const auto returned = returns
			? QGenericReturnArgument(returnType.name(), result.data())
			: QGenericReturnArgument();
		if (!method.invoke(
				widget,
				Qt::DirectConnection,
				returned,
				arguments[0], arguments[1], arguments[2], arguments[3],
				arguments[4], arguments[5], arguments[6], arguments[7],
				arguments[8], arguments[9])) {
			throw std::runtime_error("The method call failed.");
		}
		return returns ? Widgets::VariantToJson(result) : QJsonValue();
	}
	throw std::runtime_error(lastError);
}

QJsonArray Methods(not_null<QWidget*> widget) {
	auto result = QJsonArray();
	const auto meta = widget->metaObject();
	for (auto i = 0; i != meta->methodCount(); ++i) {
		const auto method = meta->method(i);
		if (method.access() != QMetaMethod::Public
			|| method.methodType() == QMetaMethod::Constructor) {
			continue;
		}
		result.push_back(QJsonObject{
			{ u"name"_q, QString::fromLatin1(method.name()) },
			{ u"signature"_q, QString::fromLatin1(method.methodSignature()) },
			{ u"type"_q, MethodType(method) },
			{ u"returns"_q, QString::fromLatin1(method.typeName()) },
		});
	}
	return result;
}

void EnsureFilter() {
	auto &state = Get();
	if (!state.filter) {
		state.filter = std::make_unique<WindowFilter>();
		qApp->installEventFilter(state.filter.get());
	}
}

void Disconnect(const QString &ruleId) {
	auto &connections = Get().connections;
	if (const auto i = connections.find(ruleId); i != end(connections)) {
		delete i->second.relay.data();
		connections.erase(i);
	}
}

} // namespace

void SetEventSender(std::function<void(QJsonObject)> send) {
	Get().send = std::move(send);
}

void Handle(const QJsonObject &command) {
	const auto method = command.value(u"method"_q).toString();
	const auto pluginId = command.value(u"plugin_id"_q).toString();
	const auto ruleId = command.value(u"rule_id"_q).toString();
	if (ruleId.isEmpty()) {
		throw std::runtime_error("A native rule needs an ID.");
	}
	auto &state = Get();
	if (method == u"ui.native.windows"_q) {
		if (command.value(u"enabled"_q).toBool()) {
			state.windowWatchers[ruleId] = pluginId;
			EnsureFilter();
		} else {
			state.windowWatchers.erase(ruleId);
		}
	} else if (method == u"ui.native.connect"_q) {
		const auto widget = Required(command.value(u"handle"_q));
		const auto signal = FindSignal(
			widget->metaObject(),
			command.value(u"signal"_q).toString());
		Disconnect(ruleId);
		const auto relay = new SignalRelay(widget, signal, [=](QJsonArray args) {
			if (const auto &send = Get().send) {
				send(QJsonObject{
					{ u"plugin_id"_q, pluginId },
					{ u"type"_q, u"native_signal"_q },
					{ u"rule_id"_q, ruleId },
					{ u"value"_q, args },
				});
			}
		});
		state.connections[ruleId] = Connection{ pluginId, relay };
	} else if (method == u"ui.native.disconnect"_q) {
		Disconnect(ruleId);
		state.windowWatchers.erase(ruleId);
	} else {
		throw std::runtime_error("Unknown native command.");
	}
}

QJsonValue Request(const QJsonObject &command) {
	const auto method = command.value(u"method"_q).toString();
	const auto widget = Required(command.value(u"handle"_q));
	if (method == u"native.methods"_q) {
		return Methods(widget);
	} else if (method == u"native.invoke"_q) {
		return Invoke(widget, command);
	}
	throw std::runtime_error("Unknown native request.");
}

void RemovePlugin(const QString &pluginId) {
	auto &state = Get();
	std::erase_if(state.windowWatchers, [&](const auto &entry) {
		return entry.second == pluginId;
	});
	for (auto i = begin(state.connections); i != end(state.connections);) {
		if (i->second.pluginId == pluginId) {
			delete i->second.relay.data();
			i = state.connections.erase(i);
		} else {
			++i;
		}
	}
}

} // namespace Ovygram::Native
