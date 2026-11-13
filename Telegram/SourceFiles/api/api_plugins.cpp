#include "api/api_plugins.h"
#include "ovygram/plugin_install.h"

#include "api/api_text_entities.h"
#include "api/api_updates.h"
#include "apiwrap.h"
#include "core/application.h"
#include "core/plugin_runtime.h"
#include "data/data_channel.h"
#include "data/data_document.h"
#include "data/data_media_types.h"
#include "data/data_peer.h"
#include "data/data_photo.h"
#include "data/data_session.h"
#include "data/data_user.h"
#include "dialogs/dialogs_key.h"
#include "history/history.h"
#include "history/history_item.h"
#include "main/main_account.h"
#include "main/main_domain.h"
#include "main/main_session.h"
#include "mtproto/facade.h"
#include "ovygram/plugin_elements.h"
#include "ovygram/plugin_menus.h"
#include "ovygram/plugin_native.h"
#include "ovygram/plugin_ui.h"
#include "ovygram/plugin_widgets.h"
#include "ui/image/image_location.h"
#include "ui/toast/toast.h"
#include "window/window_controller.h"
#include "window/window_session_controller.h"

#include <QtCore/QJsonDocument>
#include <QtCore/QPointer>
#include <QtCore/QThread>
#include <QtCore/QTimer>
#include <algorithm>
#include <cstring>
#include <set>
#include <stdexcept>

namespace Api {
namespace {

constexpr auto kMaximumPayload = 64 * 1024 * 1024;

// Whether messages returned by this request belong to the chat history.
[[nodiscard]] bool LocalHistoryRequest(const QByteArray &data) {
	if (data.size() < int(sizeof(mtpTypeId))) {
		return false;
	}
	const auto type = *reinterpret_cast<const mtpTypeId*>(data.constData());
	switch (type) {
	case mtpc_messages_getScheduledHistory:
	case mtpc_messages_getScheduledMessages:
	case mtpc_messages_getQuickReplyMessages:
		return false;
	}
	return true;
}

class HookCancellation final : public std::runtime_error {
public:
	using std::runtime_error::runtime_error;
};

QString AccountId(const Main::Session &session) {
	return QString::number(session.uniqueId());
}

template <typename Value>
QString Encode(const Value &value) {
	auto buffer = mtpBuffer();
	value.template write<mtpBuffer>(buffer);
	return QString::fromLatin1(QByteArray(
		reinterpret_cast<const char*>(buffer.constData()),
		buffer.size() * sizeof(mtpPrime)).toBase64());
}

QByteArray Decode(const QJsonValue &value) {
	const auto data = QByteArray::fromBase64(
		value.toString().toLatin1(),
		QByteArray::AbortOnBase64DecodingErrors);
	if (data.isEmpty() || data.size() > kMaximumPayload || data.size() % 4) {
		throw std::runtime_error("Invalid TL payload.");
	}
	return data;
}

mtpBuffer Buffer(const QByteArray &data) {
	auto result = mtpBuffer(data.size() / sizeof(mtpPrime));
	memcpy(result.data(), data.constData(), data.size());
	return result;
}

QJsonObject Chat(Main::Session &session, not_null<PeerData*> peer) {
	return {
		{ u"account_id"_q, AccountId(session) },
		{ u"id"_q, QString::number(peer->id.value) },
		{ u"name"_q, peer->name() },
		{ u"input_peer"_q, Encode(peer->input()) },
		{ u"kind"_q, peerIsChannel(peer->id)
			? u"channel"_q : peerIsChat(peer->id) ? u"chat"_q : u"user"_q },
	};
}

QJsonObject Message(Main::Session &session, not_null<HistoryItem*> item) {
	auto result = QJsonObject{
		{ u"account_id"_q, AccountId(session) },
		{ u"id"_q, double(item->id.bare) },
		{ u"chat_id"_q, QString::number(item->history()->peer->id.value) },
		{ u"text"_q, item->originalText().text },
		{ u"date"_q, double(item->date()) },
		{ u"outgoing"_q, item->out() },
	};
	const auto media = item->media();
	if (!media) {
		return result;
	}
	if (const auto document = media->document()) {
		const auto location = document->videoPreloadLocation();
		if (location.valid()) {
			result.insert(u"attachment"_q, QJsonObject{
				{ u"location"_q, Encode(location.tl(session.userId())) },
				{ u"dc_id"_q, location.dcId() },
				{ u"size"_q, double(document->size) },
				{ u"id"_q, QString::number(document->id) },
				{ u"name"_q, document->filename() },
				{ u"mime_type"_q, document->mimeString() },
			});
		}
	} else if (const auto photo = media->photo()) {
		const auto &file = photo->location(Data::PhotoSize::Large).file();
		if (const auto location = std::get_if<StorageFileLocation>(&file.data)) {
			if (location->valid()) {
				result.insert(u"attachment"_q, QJsonObject{
					{ u"location"_q, Encode(location->tl(session.userId())) },
					{ u"dc_id"_q, location->dcId() },
					{ u"size"_q, photo->imageByteSize(Data::PhotoSize::Large) },
					{ u"name"_q, QString::number(photo->id) + u".jpg"_q },
					{ u"mime_type"_q, u"image/jpeg"_q },
				});
			}
		}
	}
	return result;
}

QJsonObject RpcError(const MTP::Error &error) {
	return {
		{ u"code"_q, error.code() },
		{ u"name"_q, error.type() },
		{ u"description"_q, error.description() },
	};
}

} // namespace

PluginClient::PluginClient(not_null<Core::PluginRuntime*> runtime)
: _runtime(runtime) {
	Core::App().domain().accountsChanges(
	) | rpl::on_next([=] { watchAccounts(); }, _lifetime);
	Core::App().domain().activeSessionChanges(
	) | rpl::on_next([=](Main::Session *session) {
		if (session) {
			emitEvent({
				{ u"point"_q, u"account_changed"_q },
				{ u"account_id"_q, AccountId(*session) },
			});
		}
	}, _lifetime);
	watchAccounts();
	Ovygram::Menus::SetDescriber([](
			Main::Session &session,
			PeerData *peer,
			HistoryItem *item) {
		auto result = QJsonObject();
		if (peer) {
			result.insert(u"chat"_q, Chat(session, peer));
		}
		if (item) {
			result.insert(u"message"_q, Message(session, item));
		}
		return result;
	});
	_ui = std::make_unique<Ovygram::PluginUi>([=](QJsonObject event) {
		try {
			dispatch({
				{ u"action"_q, u"ui_event"_q },
				{ u"event"_q, event },
			});
		} catch (const std::exception &error) {
			LOG(("Ovygram UI event: %1").arg(QString::fromUtf8(error.what())));
		}
	});
	_runtime->setClient([=](const std::string &request) {
		const auto data = QByteArray::fromStdString(request);
		crl::on_main(this, [=] { receive(data); });
	});
	const auto registryTimer = new QTimer(this);
	connect(registryTimer, &QTimer::timeout, this, [=] {
		if (Ovygram::InstallationUiActive()) return;
		try {
			for (const auto &notice : dispatch({ { u"action"_q, u"poll"_q } }).toArray()) {
				notifyHookError(notice.toString());
			}
		} catch (const std::exception &error) {
			LOG(("Ovygram registry: %1").arg(QString::fromUtf8(error.what())));
		}
	});
	registryTimer->start(1000);
}

PluginClient::~PluginClient() {
	_runtime->setClient({});
	while (!_pending.empty()) {
		cancel(_pending.begin()->first);
	}
}

void PluginClient::watchAccounts() {
	_accountLifetime.destroy();
	for (const auto &entry : Core::App().domain().accounts()) {
		entry.account->sessionChanges(
		) | rpl::on_next([=] { synchronize(); }, _accountLifetime);
	}
	synchronize();
}

void PluginClient::synchronize() {
	auto current = std::map<QString, base::weak_ptr<Main::Session>>();
	for (const auto &entry : Core::App().domain().accounts()) {
		if (const auto session = entry.account->maybeSession()) {
			current.emplace(AccountId(*session), base::make_weak(session));
		}
	}
	auto lost = std::vector<QString>();
	for (const auto &[id, request] : _pending) {
		const auto replacement = current.find(request.accountId);
		if (!request.session || replacement == current.end()
			|| replacement->second.get() != request.session.get()) {
			lost.push_back(id);
		}
	}
	for (const auto &id : lost) {
		fail(id, u"ACCOUNT_CLOSED"_q, u"Аккаунт закрыт во время запроса."_q);
		cancel(id);
	}
	auto changedAccounts = std::set<QString>();
	for (const auto &[id, session] : _sessions) {
		changedAccounts.insert(id);
	}
	for (const auto &[id, session] : current) {
		changedAccounts.insert(id);
	}
	_sessions = std::move(current);
	for (const auto &id : changedAccounts) {
		emitEvent({ { u"point"_q, u"accounts_changed"_q }, { u"account_id"_q, id } });
	}
}

Main::Session *PluginClient::session(const QString &accountId) const {
	const auto found = _sessions.find(accountId);
	return found == _sessions.end() ? nullptr : found->second.get();
}

Main::Session *PluginClient::session(MTP::Instance *instance) const {
	for (const auto &[id, weak] : _sessions) {
		if (weak && &weak->mtp() == instance) {
			return weak.get();
		}
	}
	return nullptr;
}

QJsonValue PluginClient::dispatch(QJsonObject request) {
	if (Ovygram::InstallationUiActive()) {
		const auto action = request.value(u"action"_q).toString();
		if (action == u"native_hook"_q) {
			const auto original = request.value(u"request"_q).toObject();
			return QJsonObject{ { u"data"_q, original.value(u"data"_q) }, { u"error"_q, original.value(u"error"_q) } };
		} else if (action == u"client_event"_q || action == u"ui_event"_q || action == u"ui_execute"_q) {
			return QJsonValue();
		}
	}
	const auto response = _runtime->dispatch(
		QJsonDocument(request).toJson(QJsonDocument::Compact).toStdString());
	const auto value = QJsonDocument::fromJson(QByteArray::fromStdString(response)).object();
	if (!value.contains(u"result"_q)) {
		const auto error = value.value(u"error"_q).toString().toStdString();
		if (value.value(u"cancelled"_q).toBool()) {
			throw HookCancellation(error);
		}
		throw std::runtime_error(error);
	}
	return value.value(u"result"_q);
}

// reply() and fail() run from Qt, rpl and MTP callbacks, and from the catch
// block of receive(), where an exception would terminate the client.
void PluginClient::reply(const QString &id, QJsonValue result) {
	try {
		dispatch({
			{ u"action"_q, u"client_reply"_q },
			{ u"request"_q, QJsonObject{ { u"id"_q, id }, { u"result"_q, result } } },
		});
	} catch (const std::exception &error) {
		LOG(("Ovygram reply: %1").arg(QString::fromUtf8(error.what())));
	}
}

void PluginClient::fail(
		const QString &id,
		const QString &name,
		const QString &description,
		int code) {
	try {
		dispatch({
			{ u"action"_q, u"client_reply"_q },
			{ u"request"_q, QJsonObject{
				{ u"id"_q, id },
				{ u"error"_q, QJsonObject{
					{ u"code"_q, code },
					{ u"name"_q, name },
					{ u"description"_q, description },
				} },
			} },
		});
	} catch (const std::exception &error) {
		LOG(("Ovygram reply: %1").arg(QString::fromUtf8(error.what())));
	}
}

void PluginClient::receive(const QByteArray &request) {
	const auto command = QJsonDocument::fromJson(request).object();
	const auto id = command.value(u"id"_q).toString();
	try {
		if (id.isEmpty() || request.size() > kMaximumPayload) {
			throw std::runtime_error("Invalid client command.");
		}
		const auto method = command.value(u"method"_q).toString();
		if (Ovygram::InstallationUiActive() && method != u"ui.close_plugin"_q
			&& (method.startsWith(u"ui."_q) || method.startsWith(u"native."_q)
				|| method.startsWith(u"widgets."_q) || method.startsWith(u"compose."_q)
				|| method == u"python_ui"_q)) {
			throw std::runtime_error("Plugin UI access is suspended during installation.");
		}
		if (method.startsWith(u"ui."_q)) {
			try {
				_ui->handle(command);
			} catch (const std::exception &error) {
				dispatch({
					{ u"action"_q, u"ui_event"_q },
					{ u"event"_q, QJsonObject{
						{ u"installation_id"_q, command.value(u"installation_id"_q) },
						{ u"object_id"_q, command.value(u"object_id"_q) },
						{ u"type"_q, u"error"_q },
						{ u"value"_q, QString::fromUtf8(error.what()) },
						{ u"closed"_q, method == u"ui.show"_q },
					} },
				});
			}
			return;
		}
		if (method == u"cancel"_q) {
			const auto pending = _pending.find(id);
			if (pending != _pending.end()
				&& pending->second.installationId == command.value(u"installation_id"_q).toString()) {
				cancel(id);
			}
			return;
		}
		if (!dispatch({
				{ u"action"_q, u"client_pending"_q },
				{ u"request_id"_q, id },
				{ u"installation_id"_q, command.value(u"installation_id"_q) },
			}).toBool()) {
			return;
		}
		if (method.startsWith(u"compose."_q)) {
			reply(id, Ovygram::Elements::Request(command));
			return;
		} else if (method.startsWith(u"widgets."_q)) {
			reply(id, Ovygram::Widgets::Request(command));
			return;
		} else if (method.startsWith(u"native."_q)) {
			reply(id, Ovygram::Native::Request(command));
			return;
		} else if (method == u"python_ui"_q) {
			reply(id, dispatch({
				{ u"action"_q, u"ui_execute"_q },
				{ u"call_id"_q, command.value(u"call_id"_q) },
			}));
			return;
		} else if (method == u"accounts"_q) {
			auto accounts = QJsonArray();
			const auto active = Core::App().domain().started()
				? Core::App().domain().active().maybeSession()
				: nullptr;
			for (const auto &[accountId, weak] : _sessions) {
				if (weak) {
					accounts.push_back(QJsonObject{
						{ u"id"_q, accountId },
						{ u"user_id"_q, QString::number(weak->userId().bare) },
						{ u"name"_q, weak->user()->name() },
						{ u"active"_q, weak.get() == active },
						{ u"test_mode"_q, weak->isTestMode() },
					});
				}
			}
			reply(id, accounts);
			return;
		}
		const auto accountId = command.value(u"account_id"_q).toString();
		const auto owner = session(accountId);
		if (!owner || owner->account().loggingOut()) {
			fail(id, u"ACCOUNT_CLOSED"_q, u"Аккаунт недоступен."_q);
			return;
		}
		if (method == u"rpc"_q) {
			rpc(command, owner);
			return;
		} else if (method == u"current_chat"_q) {
			const auto &windows = Core::App().windowStack();
			for (auto i = windows.rbegin(); i != windows.rend(); ++i) {
				const auto controller = (*i)->sessionController();
				if (controller && &controller->session() == owner) {
					if (const auto history = controller->activeChatCurrent().history()) {
						reply(id, Chat(*owner, history->peer));
						return;
					}
				}
			}
			reply(id, QJsonValue(QJsonValue::Null));
			return;
		} else if (method == u"get_user"_q) {
			const auto user = owner->data().userLoaded(UserId(command.value(u"user_id"_q).toString().toULongLong()));
			if (!user) {
				throw std::runtime_error("User is not loaded.");
			}
			reply(id, QJsonObject{
				{ u"account_id"_q, accountId },
				{ u"id"_q, QString::number(user->id.to<UserId>().bare) },
				{ u"first_name"_q, user->firstName },
				{ u"last_name"_q, user->lastName },
				{ u"username"_q, user->username() },
				{ u"access_hash"_q, QString::number(user->accessHash()) },
			});
			return;
		}
		const auto peer = owner->data().peerLoaded(PeerId(command.value(u"chat_id"_q).toString().toULongLong()));
		if (!peer) {
			throw std::runtime_error("Chat is not loaded.");
		}
		if (method == u"get_chat"_q) {
			reply(id, Chat(*owner, peer));
		} else if (method == u"get_message"_q) {
			const auto item = owner->data().message(peer, MsgId(command.value(u"message_id"_q).toInteger()));
			reply(id, item ? QJsonValue(Message(*owner, item)) : QJsonValue(QJsonValue::Null));
		} else {
			throw std::runtime_error("Unknown client command.");
		}
	} catch (const std::exception &error) {
		fail(id, u"SDK_ERROR"_q, QString::fromUtf8(error.what()));
	}
}

void PluginClient::rpc(const QJsonObject &command, not_null<Main::Session*> owner) {
	const auto data = Decode(command.value(u"data"_q));
	const auto id = command.value(u"id"_q).toString();
	if (_pending.contains(id)) {
		throw std::runtime_error("Request ID is already pending.");
	}
	const auto requestId = MTP::details::GetNextRequestId();
	auto request = MTP::details::SerializedRequest::Prepare(data.size() / sizeof(mtpPrime));
	const auto offset = MTP::details::SerializedRequest::kMessageBodyPosition;
	request->resize(offset + data.size() / sizeof(mtpPrime));
	memcpy(request->data() + offset, data.constData(), data.size());
	_pending.emplace(id, Pending{
		base::make_weak(owner.get()),
		AccountId(*owner),
		command.value(u"installation_id"_q).toString(),
		requestId,
		command.value(u"hook_stack"_q).toArray(),
	});
	const auto weak = base::make_weak(owner.get());
	const auto guard = QPointer(this);
	const auto done = [=](const MTP::Response &response) {
		if (!guard || !_pending.contains(id) || !weak) {
			return true;
		}
		_pending.erase(id);
		const auto &buffer = response.reply;
		const auto encoded = QString::fromLatin1(QByteArray(
			reinterpret_cast<const char*>(buffer.constData()),
			buffer.size() * sizeof(mtpPrime)).toBase64());
		auto updates = MTPUpdates();
		auto affected = MTPmessages_AffectedMessages();
		auto from = buffer.constData();
		const auto till = buffer.constData() + buffer.size();
		if (command.value(u"feed"_q).toString() == u"delete"_q) {
			if (affected.read(from, till) && from == till) {
				// Delete locally first: the affected pts only say that
				// the deletion is already applied.
				const auto peerId = PeerId(command.value(u"chat_id"_q).toString().toULongLong());
				auto ids = QVector<MTPint>();
				for (const auto &value : command.value(u"message_ids"_q).toArray()) {
					ids.push_back(MTP_int(value.toInteger()));
				}
				if (peerIsChannel(peerId)) {
					weak->data().processMessagesDeleted(peerId, ids);
					if (const auto peer = weak->data().peerLoaded(peerId)) {
						weak->api().applyAffectedMessages(peer, affected);
					}
				} else {
					weak->data().processNonChannelMessagesDeleted(ids);
					// Outside channels the pts are common, any such peer works.
					weak->api().applyAffectedMessages(weak->user(), affected);
				}
			}
		} else if (updates.read(from, till) && from == till) {
			weak->api().updates().applyUpdates(updates);
		} else if (!LocalHistoryRequest(data)) {
			// Scheduled messages and quick replies have their own message
			// IDs and don't belong to the chat history.
		} else {
			auto messages = MTPmessages_Messages();
			from = buffer.constData();
			if (messages.read(from, from + buffer.size()) && from == buffer.constData() + buffer.size()) {
				if (command.value(u"feed"_q).toString() == u"new"_q) {
					// A message the plugin sent itself: the short sent reply has
					// no local message to fill, so add it to the history.
					messages.match([](const MTPDmessages_messagesNotModified &) {
					}, [&](const auto &data) {
						weak->data().processUsers(data.vusers());
						weak->data().processChats(data.vchats());
						for (const auto &message : data.vmessages().v) {
							weak->data().addNewMessage(
								message,
								MessageFlags(),
								NewMessageType::Unread);
						}
					});
				} else {
					const auto peerId = PeerId(command.value(u"chat_id"_q).toString().toULongLong());
					const auto channel = peerIsChannel(peerId)
						? weak->data().channelLoaded(peerToChannel(peerId))
						: nullptr;
					weak->data().processExistingMessages(channel, messages);
				}
			}
		}
		reply(id, QJsonObject{ { u"data"_q, encoded } });
		return true;
	};
	const auto failed = [=](const MTP::Error &error, const MTP::Response &response) {
		if (guard && _pending.erase(id)) {
			fail(id, error.type(), error.description(), error.code());
		}
		return true;
	};
	const auto dc = command.value(u"dc_id"_q).toInt();
	owner->mtp().sendSerialized(
		requestId,
		std::move(request),
		{ done, failed },
		dc ? MTP::downloadDcId(dc, 0) : 0,
		0,
		0);
	const auto timeout = std::clamp(command.value(u"timeout"_q).toInt(60), 1, 300);
	QTimer::singleShot(timeout * 1000, this, [=] {
		if (_pending.contains(id)) {
			fail(id, u"TIMEOUT"_q, u"Время ожидания ответа истекло."_q);
			cancel(id);
		}
	});
}

void PluginClient::cancel(const QString &id) {
	const auto found = _pending.find(id);
	if (found == _pending.end()) {
		return;
	}
	if (const auto owner = found->second.session.get()) {
		owner->mtp().cancel(found->second.requestId);
	}
	_pending.erase(found);
}

void PluginClient::emitEvent(QJsonObject event) {
	try {
		dispatch({
			{ u"action"_q, u"client_event"_q },
			{ u"event"_q, event },
		});
	} catch (const std::exception &error) {
		LOG(("Ovygram event: %1").arg(QString::fromUtf8(error.what())));
	}
}

void PluginClient::chatChanged(Main::Session &session, PeerData *peer) {
	emitEvent({
		{ u"point"_q, u"chat_changed"_q },
		{ u"account_id"_q, AccountId(session) },
		{ u"chat"_q, peer ? QJsonValue(Chat(session, peer)) : QJsonValue(QJsonValue::Null) },
	});
}

void PluginClient::notifyHookError(const QString &text) {
	LOG(("Ovygram hook: %1").arg(text));
	if (const auto window = Core::App().activeWindow()) {
		if (const auto controller = window->sessionController()) {
			controller->showToast(text);
		}
	}
}

bool PluginClient::beforeRpc(
		MTP::Instance *instance,
		mtpRequestId requestId,
		MTP::details::SerializedRequest &request,
		MTP::ResponseHandler &callbacks) {
	const auto owner = session(instance);
	if (!owner || !(_runtime->hookMask() & 7U)) {
		return true;
	}
	const auto accountId = AccountId(*owner);
	const auto weak = base::make_weak(owner);
	const auto reject = [&](const QString &type, const QString &message) {
		notifyHookError(message);
		// Complete after Sender and Histories have registered the request.
		// The handlers stay in MTP::Instance, so a request cancelled
		// meanwhile (its Sender destroyed, for example) gets no callback.
		QTimer::singleShot(0, this, [=] {
			if (weak) {
				auto reply = mtpBuffer();
				MTP::Error::MTPLocal(type, message).write(reply);
				weak->mtp().processCallback(
					MTP::Response{ std::move(reply), 0, requestId });
			}
		});
		return false;
	};
	auto requestData = QString();
	auto stack = QJsonArray();
	for (const auto &[id, pending] : _pending) {
		if (pending.requestId == requestId) {
			stack = pending.hookStack;
			break;
		}
	}
	try {
		const auto offset = MTP::details::SerializedRequest::kMessageBodyPosition;
		const auto data = QByteArray(
			reinterpret_cast<const char*>(request->constData() + offset),
			(*request)[MTP::details::SerializedRequest::kMessageLengthPosition]);
		requestData = QString::fromLatin1(data.toBase64());
		const auto result = dispatch({
			{ u"action"_q, u"native_hook"_q },
			{ u"request"_q, QJsonObject{
				{ u"point"_q, u"before_rpc"_q },
				{ u"account_id"_q, accountId },
				{ u"request_id"_q, requestId },
				{ u"hook_stack"_q, stack },
				{ u"data"_q, QString::fromLatin1(data.toBase64()) },
			} },
		}).toObject();
		const auto changed = Decode(result.value(u"data"_q));
		auto replacement = MTP::details::SerializedRequest::Prepare(changed.size() / sizeof(mtpPrime));
		replacement->resize(offset + changed.size() / sizeof(mtpPrime));
		memcpy(replacement->data() + offset, changed.constData(), changed.size());
		auto localTexts = std::vector<std::pair<uint64, TextWithEntities>>();
		for (const auto &entry : result.value(u"local_texts"_q).toArray()) {
			const auto object = entry.toObject();
			const auto buffer = Buffer(Decode(object.value(u"text"_q)));
			auto from = buffer.constData();
			auto text = MTPTextWithEntities();
			if (!text.read(from, from + buffer.size()) || from != buffer.constData() + buffer.size()) {
				throw std::runtime_error("Invalid modified message text.");
			}
			localTexts.emplace_back(
				uint64(object.value(u"random_id"_q).toString().toLongLong()),
				ParseTextWithEntities(owner, text));
		}
		request = std::move(replacement);
		requestData = QString::fromLatin1(changed.toBase64());
		for (auto &[randomId, text] : localTexts) {
			if (const auto item = owner->data().message(owner->data().messageIdByRandomId(randomId))) {
				// Registration keeps an existing entry, and a short sent
				// update restores the message text from that entry.
				owner->data().unregisterMessageSentData(randomId);
				owner->data().registerMessageSentData(randomId, item->history()->peer->id, text.text);
				item->setText(std::move(text));
				// setText() repaints only a message that had text before,
				// and a media message may have had no caption.
				owner->data().requestItemTextRefresh(item);
				item->history()->updateChatListEntry();
			}
		}
	} catch (const HookCancellation &error) {
		return reject(u"PLUGIN_CANCELLED"_q, QString::fromUtf8(error.what()));
	} catch (const std::exception &error) {
		return reject(u"PLUGIN_HOOK"_q, QString::fromUtf8(error.what()));
	}
	const auto original = std::make_shared<MTP::ResponseHandler>(std::move(callbacks));
	const auto guard = QPointer(this);
	// Set once after_rpc saw the response: if the caller then fails to parse
	// it, MTP reports a parse error to fail(), which must not run it again.
	const auto handled = std::make_shared<bool>(false);
	callbacks.done = [=](const MTP::Response &response) mutable {
		if (!guard) {
			return original->done ? original->done(response) : true;
		}
		if (!weak) {
			return true;
		}
		*handled = true;
		auto changed = response;
		auto error = std::optional<MTP::Error>();
		if (!afterRpc(accountId, requestId, requestData, stack, changed, error)) {
			error = MTP::Error::Local(u"PLUGIN_HOOK"_q, u"Ошибка обработки ответа плагином."_q);
		}
		if (error) {
			return original->fail ? original->fail(*error, changed) : false;
		}
		return original->done ? original->done(changed) : true;
	};
	callbacks.fail = [=](
			const MTP::Error &error,
			const MTP::Response &response) {
		// A temporary error (flood wait, server error) is usually retried by
		// MTP, and after_rpc sees the final result instead.
		if (!guard || *handled || MTP::IsTemporaryError(error)) {
			return original->fail ? original->fail(error, response) : false;
		}
		if (!weak) {
			return true;
		}
		*handled = true;
		auto changed = response;
		auto changedError = std::optional<MTP::Error>(error);
		if (!afterRpc(accountId, requestId, requestData, stack, changed, changedError)) {
			changedError = MTP::Error::Local(u"PLUGIN_HOOK"_q, u"Ошибка обработки ответа плагином."_q);
		}
		if (changedError) {
			return original->fail ? original->fail(*changedError, changed) : false;
		}
		return original->done ? original->done(changed) : true;
	};
	return true;
}

bool IsPluginRpcCancelled(const MTP::Error &error) {
	return error.code() == 0 && error.type() == u"CLIENT_PLUGIN_CANCELLED"_q;
}

bool PluginClient::afterRpc(
		const QString &accountId,
		mtpRequestId requestId,
		const QString &requestData,
		const QJsonArray &hookStack,
		MTP::Response &response,
		std::optional<MTP::Error> &error) {
	if (!(_runtime->hookMask() & (1U << 2))) {
		return true;
	}
	try {
		const auto encoded = QString::fromLatin1(QByteArray(
			reinterpret_cast<const char*>(response.reply.constData()),
			response.reply.size() * sizeof(mtpPrime)).toBase64());
		const auto result = dispatch({
			{ u"action"_q, u"native_hook"_q },
			{ u"request"_q, QJsonObject{
				{ u"point"_q, u"after_rpc"_q },
				{ u"account_id"_q, accountId },
				{ u"request_id"_q, requestId },
				{ u"request_data"_q, requestData },
				{ u"hook_stack"_q, hookStack },
				{ u"data"_q, error ? QString() : encoded },
				{ u"error"_q, error ? QJsonValue(RpcError(*error)) : QJsonValue(QJsonValue::Null) },
			} },
		}).toObject();
		if (result.value(u"error"_q).isObject()) {
			const auto changed = result.value(u"error"_q).toObject();
			auto code = changed.value(u"code"_q).toInt();
			auto name = changed.value(u"name"_q).toString();
			if (code < 0 || code >= 500) {
				// MTP would resend the request for these codes.
				code = 400;
			}
			if (MTP::IsFloodError(name)) {
				name = u"PLUGIN_"_q + name;
			}
			error = MTP::Error(MTP_rpc_error(
				MTP_int(code),
				MTP_bytes((name
					+ u": "_q + changed.value(u"description"_q).toString()).toUtf8())));
		} else {
			response.reply = Buffer(Decode(result.value(u"data"_q)));
			error.reset();
		}
		return true;
	} catch (const HookCancellation &failure) {
		notifyHookError(QString::fromUtf8(failure.what()));
		return false;
	} catch (const std::exception &failure) {
		// A broken hook must not break Telegram: keep the server answer.
		notifyHookError(QString::fromUtf8(failure.what()));
		return true;
	}
}

bool PluginClient::beforeUpdates(Main::Session &session, MTPUpdates &updates) {
	if (!(_runtime->hookMask() & (1U << 3))) {
		return true;
	}
	try {
		const auto result = dispatch({
			{ u"action"_q, u"native_hook"_q },
			{ u"request"_q, QJsonObject{
				{ u"point"_q, u"before_updates"_q },
				{ u"account_id"_q, AccountId(session) },
				{ u"data"_q, Encode(updates) },
			} },
		}).toObject();
		const auto buffer = Buffer(Decode(result.value(u"data"_q)));
		auto from = buffer.constData();
		auto changed = MTPUpdates();
		if (!changed.read(from, from + buffer.size()) || from != buffer.constData() + buffer.size()) {
			throw std::runtime_error("Invalid modified Updates.");
		}
		updates = std::move(changed);
		return true;
	} catch (const HookCancellation &error) {
		// The hook asked to skip these updates.
		notifyHookError(QString::fromUtf8(error.what()));
		return false;
	} catch (const std::exception &error) {
		// A broken hook must not lose server updates: apply them unchanged.
		notifyHookError(QString::fromUtf8(error.what()));
		return true;
	}
}

void PluginClient::observeMessages(
		Main::Session &session,
		const MTPVector<MTPMessage> &messages) {
	if (!(_runtime->hookMask() & (1U << 4))) {
		return;
	}
	for (const auto &message : messages.v) {
		emitEvent({
			{ u"point"_q, u"raw_message"_q },
			{ u"account_id"_q, AccountId(session) },
			{ u"data"_q, Encode(message) },
		});
	}
}

void PluginClient::observeSentMessage(
		Main::Session &session,
		not_null<HistoryItem*> item) {
	if (_runtime->hookMask() & (1U << 4)) {
		emitEvent({
			{ u"point"_q, u"new_message"_q },
			{ u"account_id"_q, AccountId(session) },
			{ u"message"_q, Message(session, item) },
		});
	}
}

void PluginClient::observeUpdate(Main::Session &session, const MTPUpdate &update) {
	const auto mask = _runtime->hookMask();
	if (!(mask & ((1U << 4) | (1U << 5) | (1U << 6)))) {
		return;
	}
	switch (update.type()) {
	case mtpc_updateNewMessage:
	case mtpc_updateNewChannelMessage:
	case mtpc_updateEditMessage:
	case mtpc_updateEditChannelMessage:
	case mtpc_updateDeleteMessages:
	case mtpc_updateDeleteChannelMessages:
		break;
	default:
		return;
	}
	emitEvent({
		{ u"point"_q, u"raw_update"_q },
		{ u"account_id"_q, AccountId(session) },
		{ u"data"_q, Encode(update) },
	});
}

void PluginClient::observeUpdates(Main::Session &session, const MTPUpdates &updates) {
	if (!(_runtime->hookMask() & (1U << 4))
		|| (updates.type() != mtpc_updateShortMessage && updates.type() != mtpc_updateShortChatMessage)) {
		return;
	}
	emitEvent({
		{ u"point"_q, u"raw_updates"_q },
		{ u"account_id"_q, AccountId(session) },
		{ u"data"_q, Encode(updates) },
	});
}

bool PluginBeforeRpc(
		MTP::Instance *instance,
		mtpRequestId requestId,
		MTP::details::SerializedRequest &request,
		MTP::ResponseHandler &callbacks) {
	const auto client = Core::App().pluginClient();
	return !client || QThread::currentThread() != client->thread()
		|| client->beforeRpc(instance, requestId, request, callbacks);
}

bool PluginBeforeUpdates(Main::Session &session, MTPUpdates &updates) {
	const auto client = Core::App().pluginClient();
	return !client || client->beforeUpdates(session, updates);
}

void PluginObserveUpdate(Main::Session &session, const MTPUpdate &update) {
	if (const auto client = Core::App().pluginClient()) {
		client->observeUpdate(session, update);
	}
}

void PluginObserveUpdates(Main::Session &session, const MTPUpdates &updates) {
	if (const auto client = Core::App().pluginClient()) {
		client->observeUpdates(session, updates);
	}
}

void PluginObserveMessages(
		Main::Session &session,
		const MTPVector<MTPMessage> &messages) {
	if (const auto client = Core::App().pluginClient()) {
		client->observeMessages(session, messages);
	}
}

void PluginObserveSentMessage(
		Main::Session &session,
		not_null<HistoryItem*> item) {
	if (const auto client = Core::App().pluginClient()) {
		client->observeSentMessage(session, item);
	}
}

void PluginChatChanged(Main::Session &session, PeerData *peer) {
	if (const auto client = Core::App().pluginClient()) {
		client->chatChanged(session, peer);
	}
}

} // namespace Api
