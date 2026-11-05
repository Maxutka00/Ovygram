"""Cancellable file transfers using the client's authenticated RPC sessions."""

import asyncio
import hashlib
import inspect
import mimetypes
import os
from pathlib import Path
import secrets
import uuid

from . import tl
from .client import _chat, get_chat, get_message, rpc
from ._runtime import RpcError
from .models import Attachment, Progress


PART_SIZE = 512 * 1024


async def _progress(callback, account_id, amount, total):
    if callback is not None:
        result = callback(Progress(account_id, amount, total))
        if inspect.isawaitable(result):
            await result


async def send_file(chat, path, *, caption="", progress=None, silent=False):
    _chat(chat)
    path = Path(path).resolve(strict=True)
    size = path.stat().st_size
    if size <= 0:
        raise ValueError("Пустой файл нельзя отправить.")
    identity = secrets.randbits(63)
    total = (size + PART_SIZE - 1) // PART_SIZE
    if total > 8000:
        raise ValueError("Файл превышает предел поддерживаемой загрузки.")
    big = size > 10 * 1024 * 1024
    checksum = hashlib.md5(usedforsecurity=False)
    stream = await asyncio.to_thread(path.open, "rb")
    try:
        for part in range(total):
            data = await asyncio.to_thread(stream.read, PART_SIZE)
            if not data or (part != total - 1 and len(data) != PART_SIZE):
                raise RuntimeError("Файл изменился во время загрузки.")
            if big:
                request = tl.upload.saveBigFilePart(file_id=identity, file_part=part,
                                                    file_total_parts=total, bytes=data)
            else:
                checksum.update(data)
                request = tl.upload.saveFilePart(file_id=identity, file_part=part, bytes=data)
            if not await rpc(chat.account_id, request):
                raise RuntimeError("Telegram не принял часть файла.")
            await _progress(progress, chat.account_id, min((part + 1) * PART_SIZE, size), size)
        if stream.tell() != size or path.stat().st_size != size:
            raise RuntimeError("Файл изменился во время загрузки.")
    finally:
        await asyncio.to_thread(stream.close)
    uploaded = tl.inputFileBig(id=identity, parts=total, name=path.name) if big else tl.inputFile(
        id=identity, parts=total, name=path.name, md5_checksum=checksum.hexdigest())
    media = tl.inputMediaUploadedDocument(file=uploaded,
        mime_type=mimetypes.guess_type(path.name)[0] or "application/octet-stream",
        attributes=[tl.documentAttributeFilename(file_name=path.name)])
    return await rpc(chat.account_id, tl.messages.sendMedia(
        peer=chat.input_peer, media=media, message=caption, random_id=secrets.randbits(63), silent=silent))


async def download_file(attachment, destination, *, progress=None):
    if not isinstance(attachment, Attachment):
        raise TypeError("Ожидается Attachment с явным account_id.")
    target = Path(destination).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + ".part-" + uuid.uuid4().hex)
    stream = await asyncio.to_thread(partial.open, "xb")
    complete = False
    offset = 0
    refreshed = False
    try:
        while attachment.size <= 0 or offset < attachment.size:
            try:
                result = await rpc(attachment.account_id, tl.upload.getFile(
                    location=attachment.location, offset=offset, limit=PART_SIZE,
                    precise=True, cdn_supported=False), dc_id=attachment.dc_id)
            except RpcError as error:
                if (refreshed or not error.name.startswith("FILE_REFERENCE_")
                        or attachment.message_chat_id is None or attachment.message_id is None):
                    raise
                chat = await get_chat(attachment.account_id, attachment.message_chat_id)
                message = await get_message(chat, attachment.message_id)
                updated = message.attachment if message is not None else None
                if (updated is None or updated.location.id != attachment.location.id
                        or updated.size != attachment.size):
                    raise RuntimeError("Вложение сообщения изменилось.") from error
                attachment = updated
                refreshed = True
                continue
            if result.constructor_name != "upload.file":
                raise RuntimeError("Telegram вернул неподдерживаемый тип загрузки.")
            data = result.bytes
            if not data:
                break
            await asyncio.to_thread(stream.write, data)
            offset += len(data)
            await _progress(progress, attachment.account_id, offset, attachment.size)
            if len(data) < PART_SIZE:
                break
        if attachment.size > 0 and offset != attachment.size:
            raise RuntimeError("Скачан неполный файл.")
        await asyncio.to_thread(stream.flush)
        await asyncio.to_thread(os.fsync, stream.fileno())
        await asyncio.to_thread(stream.close)
        partial.replace(target)
        complete = True
    finally:
        if not stream.closed:
            await asyncio.to_thread(stream.close)
        if not complete:
            partial.unlink(missing_ok=True)
    return target
