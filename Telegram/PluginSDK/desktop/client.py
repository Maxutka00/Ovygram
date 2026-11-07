"""Account-explicit asynchronous Telegram operations."""

import base64
import secrets

from . import tl
from ._runtime import context
from .models import Account, Chat, User, chat_from_native, message_from_native, message_from_tl


async def _request(method, account_id=None, **parameters):
    return await context().manager.runtime.request(method, account_id, **parameters)


def _account(account):
    if isinstance(account, Account):
        return account.id
    if not isinstance(account, str) or not account:
        raise ValueError("Укажи аккаунт явно.")
    return account


async def accounts():
    return [Account(str(item["id"]), int(item["user_id"]), item["name"],
                    item["active"], item["test_mode"]) for item in await _request("accounts")]


async def current_chat(account):
    value = await _request("current_chat", _account(account))
    return chat_from_native(value) if value is not None else None


async def get_chat(account, chat_id):
    return chat_from_native(await _request("get_chat", _account(account), chat_id=str(chat_id)))


async def get_user(account, user_id):
    value = await _request("get_user", _account(account), user_id=str(user_id))
    return User(value["account_id"], int(value["id"]), value["first_name"], value["last_name"],
                value["username"], int(value["access_hash"]))


async def get_loaded_message(chat, message_id):
    _chat(chat)
    value = await _request("get_message", chat.account_id, chat_id=str(chat.id), message_id=message_id)
    return message_from_native(value) if value is not None else None


def _chat(chat):
    if not isinstance(chat, Chat):
        raise TypeError("Ожидается Chat с явным account_id.")
    return chat


async def rpc(account, request, *, dc_id=0, timeout=60, _feed=""):
    account_id = _account(account)
    if not isinstance(request, tl.TLObject) or not request._tl["function"]:
        raise TypeError("Ожидается TL-запрос из desktop.tl.")
    data = base64.b64encode(tl.encode(request)).decode("ascii")
    peer = getattr(request, "peer", None) or getattr(request, "channel", None)
    chat_id = ""
    if peer is not None:
        if peer.constructor_name in ("inputPeerChannel", "inputChannel"):
            chat_id = str(peer.channel_id | (2 << 48))
        elif peer.constructor_name == "inputPeerChat":
            chat_id = str(peer.chat_id | (1 << 48))
        elif peer.constructor_name == "inputPeerUser":
            chat_id = str(peer.user_id)
    response = await _request("rpc", account_id, data=data, dc_id=dc_id,
                              timeout=timeout, chat_id=chat_id, feed=_feed)
    return tl.decode(base64.b64decode(response["data"], validate=True), tl.response_type(request))


async def history(chat, *, limit=50, offset_id=0):
    _chat(chat)
    if not 1 <= limit <= 100:
        raise ValueError("Лимит истории должен быть от 1 до 100.")
    result = await rpc(chat.account_id, tl.messages.getHistory(
        peer=chat.input_peer, offset_id=offset_id, offset_date=0,
        add_offset=0, limit=limit, max_id=0, min_id=0, hash=0))
    return [message_from_tl(chat.account_id, item) for item in result.messages
            if item.constructor_name in ("message", "messageService")]


async def send_message(chat, text, *, reply_to=None, silent=False, no_webpage=False):
    _chat(chat)
    if not isinstance(text, str) or not text:
        raise ValueError("Текст сообщения пуст.")
    reply = tl.inputReplyToMessage(reply_to_msg_id=reply_to) if reply_to is not None else None
    result = await rpc(chat.account_id, tl.messages.sendMessage(
        peer=chat.input_peer, message=text, random_id=secrets.randbits(63),
        reply_to=reply, silent=silent, no_webpage=no_webpage))
    if result.constructor_name == "updateShortSentMessage":
        message = await _fetch_message(chat, result.id, "new")
        if message is not None:
            from desktop_utils import run_on_ui
            from .models import Event
            await run_on_ui(lambda: context().manager.runtime.emit(
                "new_message", Event(chat.account_id, message=message, chat_id=chat.id)))
    return result


async def edit_message(chat, message_id, text):
    _chat(chat)
    return await rpc(chat.account_id, tl.messages.editMessage(
        peer=chat.input_peer, id=message_id, message=text))


async def delete_messages(chat, message_ids, *, revoke=True):
    _chat(chat)
    ids = list(message_ids)
    if chat.kind == "channel":
        peer = chat.input_peer
        return await rpc(chat.account_id, tl.channels.deleteMessages(
            channel=tl.inputChannel(channel_id=peer.channel_id, access_hash=peer.access_hash), id=ids))
    return await rpc(chat.account_id, tl.messages.deleteMessages(id=ids, revoke=revoke))


async def forward_messages(source, target, message_ids, *, silent=False):
    _chat(source)
    _chat(target)
    if source.account_id != target.account_id:
        raise ValueError("Пересылка требует чаты одного аккаунта.")
    ids = list(message_ids)
    return await rpc(source.account_id, tl.messages.forwardMessages(
        from_peer=source.input_peer, id=ids, random_id=[secrets.randbits(63) for _ in ids],
        to_peer=target.input_peer, silent=silent))


async def get_message(chat, message_id):
    return await _fetch_message(chat, message_id, "")


async def _fetch_message(chat, message_id, feed):
    _chat(chat)
    ids = [tl.inputMessageID(id=message_id)]
    if chat.kind == "channel":
        peer = chat.input_peer
        result = await rpc(chat.account_id, tl.channels.getMessages(
            channel=tl.inputChannel(channel_id=peer.channel_id, access_hash=peer.access_hash), id=ids),
            _feed=feed)
    else:
        result = await rpc(chat.account_id, tl.messages.getMessages(id=ids), _feed=feed)
    return next((message_from_tl(chat.account_id, item) for item in result.messages
                 if item.constructor_name in ("message", "messageService")), None)
