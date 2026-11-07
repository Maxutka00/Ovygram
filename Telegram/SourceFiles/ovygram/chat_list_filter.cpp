#include "ovygram/chat_list_filter.h"

#include "core/application.h"
#include "data/data_peer.h"
#include "data/data_session.h"
#include "dialogs/dialogs_entry.h"
#include "history/history.h"
#include "main/main_account.h"
#include "main/main_domain.h"
#include "main/main_session.h"

#include <QtCore/QJsonArray>

#include <map>
#include <set>
#include <stdexcept>
#include <vector>

namespace Ovygram {
namespace {

struct Rule {
	QString pluginId;
	QString accountId;
	std::set<QString> chatIds;
};

std::map<QString, Rule> &Rules() {
	static auto result = std::map<QString, Rule>();
	return result;
}

[[nodiscard]] Main::Session *FindSession(const QString &accountId) {
	for (const auto &entry : Core::App().domain().accounts()) {
		const auto session = entry.account->maybeSession();
		if (session && QString::number(session->uniqueId()) == accountId) {
			return session;
		}
	}
	return nullptr;
}

// Lets Telegram re-check whether each chat belongs to the chat list.
void Refresh(const QString &accountId, const std::set<QString> &chatIds) {
	const auto session = FindSession(accountId);
	if (!session) {
		return;
	}
	for (const auto &chatId : chatIds) {
		const auto peerId = PeerId(chatId.toULongLong());
		if (const auto history = session->data().historyLoaded(peerId)) {
			history->updateChatListExistence();
		}
	}
}

} // namespace

bool HiddenFromChatList(not_null<Dialogs::Entry*> entry) {
	const auto &rules = Rules();
	if (rules.empty()) {
		return false;
	}
	const auto history = entry->asHistory();
	if (!history) {
		return false;
	}
	const auto accountId = QString::number(history->session().uniqueId());
	const auto chatId = QString::number(history->peer->id.value);
	for (const auto &[id, rule] : rules) {
		if (rule.accountId == accountId && rule.chatIds.contains(chatId)) {
			return true;
		}
	}
	return false;
}

namespace ChatListFilter {

void Handle(const QJsonObject &command) {
	const auto method = command.value(u"method"_q).toString();
	const auto ruleId = command.value(u"rule_id"_q).toString();
	if (ruleId.isEmpty()) {
		throw std::runtime_error("A chat list rule needs an ID.");
	}
	auto &rules = Rules();
	if (method == u"ui.chat_list.hide"_q) {
		auto rule = Rule{
			.pluginId = command.value(u"plugin_id"_q).toString(),
			.accountId = command.value(u"account_id"_q).toString(),
		};
		for (const auto &value : command.value(u"chat_ids"_q).toArray()) {
			rule.chatIds.insert(value.toString());
		}
		if (rule.accountId.isEmpty() || rule.chatIds.empty()) {
			throw std::runtime_error("A chat list rule needs account_id and chats.");
		}
		auto refresh = rule.chatIds;
		if (const auto old = rules.find(ruleId); old != end(rules)) {
			refresh.insert(begin(old->second.chatIds), end(old->second.chatIds));
		}
		const auto accountId = rule.accountId;
		rules[ruleId] = std::move(rule);
		Refresh(accountId, refresh);
	} else if (method == u"ui.chat_list.unhide"_q) {
		const auto i = rules.find(ruleId);
		if (i != end(rules)) {
			auto rule = std::move(i->second);
			rules.erase(i);
			Refresh(rule.accountId, rule.chatIds);
		}
	} else {
		throw std::runtime_error("Unknown chat list command.");
	}
}

void RemovePlugin(const QString &pluginId) {
	auto removed = std::vector<Rule>();
	auto &rules = Rules();
	for (auto i = begin(rules); i != end(rules);) {
		if (i->second.pluginId == pluginId) {
			removed.push_back(std::move(i->second));
			i = rules.erase(i);
		} else {
			++i;
		}
	}
	for (const auto &rule : removed) {
		Refresh(rule.accountId, rule.chatIds);
	}
}

} // namespace ChatListFilter
} // namespace Ovygram
