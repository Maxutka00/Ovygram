from dataclasses import dataclass, replace

from . import tl


@dataclass(frozen=True)
class Account:
    id: str
    user_id: int
    name: str
    active: bool = False
    test_mode: bool = False


@dataclass(frozen=True)
class Chat:
    account_id: str
    id: int
    name: str
    input_peer: tl.TLObject
    kind: str


@dataclass(frozen=True)
class User:
    account_id: str
    id: int
    first_name: str
    last_name: str
    username: str = ""
    access_hash: int = 0


@dataclass(frozen=True)
class Attachment:
    account_id: str
    location: tl.TLObject
    dc_id: int
    size: int
    name: str
    mime_type: str = "application/octet-stream"
    source: tl.TLObject | None = None
    message_chat_id: int | None = None
    message_id: int | None = None


@dataclass(frozen=True)
class Message:
    account_id: str
    id: int
    chat_id: int
    text: str
    date: int
    outgoing: bool
    attachment: Attachment | None = None
    raw: tl.TLObject | None = None


@dataclass(frozen=True)
class Event:
    account_id: str
    message: Message | None = None
    chat: Chat | None = None
    message_ids: tuple[int, ...] = ()
    chat_id: int | None = None


@dataclass(frozen=True)
class Progress:
    account_id: str
    transferred: int
    total: int


def peer_id(peer):
    if peer.constructor_name == "peerUser":
        return peer.user_id
    if peer.constructor_name == "peerChat":
        return peer.chat_id | (1 << 48)
    if peer.constructor_name == "peerChannel":
        return peer.channel_id | (2 << 48)
    raise ValueError("Unknown peer type.")


def attachment(account_id, media):
    if media is None:
        return None
    document = getattr(media, "document", None)
    if document is not None and document.constructor_name == "document":
        name = next((item.file_name for item in document.attributes
                     if item.constructor_name == "documentAttributeFilename"), str(document.id))
        return Attachment(account_id, tl.inputDocumentFileLocation(
            id=document.id, access_hash=document.access_hash,
            file_reference=document.file_reference, thumb_size=""), document.dc_id,
            document.size, name, document.mime_type, document)
    photo = getattr(media, "photo", None)
    if photo is not None and photo.constructor_name == "photo":
        sizes = [item for item in photo.sizes if item.constructor_name in ("photoSize", "photoSizeProgressive")]
        if sizes:
            size = max(sizes, key=lambda item: item.w * item.h)
            length = size.size if hasattr(size, "size") else max(size.sizes, default=0)
            return Attachment(account_id, tl.inputPhotoFileLocation(
                id=photo.id, access_hash=photo.access_hash,
                file_reference=photo.file_reference, thumb_size=size.type), photo.dc_id,
                length, f"{photo.id}.jpg", "image/jpeg", photo)
    return None


def message_from_tl(account_id, value):
    chat_id = peer_id(value.peer_id)
    media = attachment(account_id, getattr(value, "media", None))
    if media is not None:
        media = replace(media, message_chat_id=chat_id, message_id=value.id)
    return Message(account_id, value.id, chat_id, getattr(value, "message", ""),
                   value.date, getattr(value, "out", False),
                   media, value)


def chat_from_native(value):
    import base64
    return Chat(value["account_id"], int(value["id"]), value["name"],
                tl.decode(base64.b64decode(value["input_peer"]), "InputPeer"), value["kind"])


def message_from_native(value):
    import base64
    media = value.get("attachment")
    file = None
    if media is not None:
        file = Attachment(value["account_id"],
            tl.decode(base64.b64decode(media["location"]), "InputFileLocation"),
            media["dc_id"], int(media["size"]), media["name"], media["mime_type"],
            message_chat_id=int(value["chat_id"]), message_id=int(value["id"]))
    return Message(value["account_id"], int(value["id"]), int(value["chat_id"]),
                   value["text"], value["date"], value["outgoing"], file)
