#pragma once

#include "base/object_ptr.h"

#include <rpl/event_stream.h>
#include <rpl/producer.h>

#include <QtCore/QJsonObject>
#include <QtCore/QObject>
#include <QtCore/QPointer>

#include <functional>
#include <map>
#include <memory>
#include <vector>

class PeerData;
class QWidget;

namespace Ui {
class RpWidget;
} // namespace Ui

namespace Ovygram {

// Builds plugin dialogs and windows from the tree sent by desktop/ui.py.
// Everything here runs on the main thread; objects belong to one plugin
// and are destroyed together with it.
class PluginUi final : public QObject {
public:
	using EventSender = std::function<void(QJsonObject)>;

	explicit PluginUi(EventSender send);
	~PluginUi();

	// Handles a "ui.*" command. Throws std::runtime_error on invalid input.
	void handle(const QJsonObject &command);

	[[nodiscard]] static PluginUi *Instance();
	[[nodiscard]] int layoutChatBars(
		QWidget *chat,
		PeerData *peer,
		int left,
		int top,
		int width);

	// For the section in the main column, see plugin_section.h.
	[[nodiscard]] Ui::RpWidget *sectionContent(const QString &objectId) const;
	[[nodiscard]] QString sectionTitle(const QString &objectId) const;
	[[nodiscard]] rpl::producer<> sectionClosed(const QString &objectId) const;
	// Nothing can show the section any more: close the surface.
	void sectionGone(const QString &objectId);

private:
	struct Object;

	void show(const QJsonObject &command);
	void update(const QJsonObject &command);
	void close(const QString &objectId, bool notify);
	void closePlugin(const QString &installationId);
	void destroyed(const QString &objectId);
	void relayoutChats();
	void relayoutChatsNow();
	[[nodiscard]] object_ptr<Ui::RpWidget> build(
		Object &object,
		QWidget *parent,
		const QJsonObject &node,
		int depth);
	void send(
		const Object &object,
		const QString &nodeId,
		const QString &type,
		QJsonValue value = QJsonValue());

	EventSender _send;
	std::map<QString, std::unique_ptr<Object>> _objects;
	std::vector<QPointer<QWidget>> _chats;
	bool _relayoutQueued = false;
	bool _updating = false;
	rpl::event_stream<QString> _sectionClosed;

};

} // namespace Ovygram
