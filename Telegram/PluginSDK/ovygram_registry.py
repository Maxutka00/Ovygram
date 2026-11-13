"""HTTPS registry transport and validation. Indexes never grant trust.

Only deployment-pinned Ed25519 keys are accepted, including for /chains.
OpenSSL is the same system/bundled libcrypto used by CPython's TLS module;
no plugin dependencies, downloaded keys or executable package code are used.
"""

import base64
import ctypes
import ctypes.util
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import unicodedata
import urllib.parse
import urllib.request

from ovygram_package import MAX_PACKAGE

TRUSTED = frozenset(("verified", "official"))
STATUSES = TRUSTED | {"unverified", "revoked", "blocked"}
UNAVAILABLE = "Сервер не отвечает — невозможно проверить плагин"


def canonical(document):
    return json.dumps({key: value for key, value in document.items() if key != "signature"},
                      sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def verify_ed25519(key, signature, payload):
    if len(key) != 32 or len(signature) != 64:
        raise ValueError("Некорректная подпись реестра.")
    if sys.platform == "win32":
        library = str(Path(sys.executable).resolve().parent / "libcrypto-3.dll")
    else:
        library = ctypes.util.find_library("crypto")
        if not library:
            raise ValueError("OpenSSL libcrypto недоступна.")
    crypto = ctypes.CDLL(library)
    crypto.EVP_PKEY_new_raw_public_key_ex.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                                   ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
    crypto.EVP_PKEY_new_raw_public_key_ex.restype = ctypes.c_void_p
    crypto.EVP_MD_CTX_new.restype = ctypes.c_void_p
    crypto.EVP_DigestVerifyInit.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
                                          ctypes.c_void_p, ctypes.c_void_p]
    crypto.EVP_DigestVerify.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t,
                                      ctypes.c_char_p, ctypes.c_size_t]
    crypto.EVP_MD_CTX_free.argtypes = [ctypes.c_void_p]
    crypto.EVP_PKEY_free.argtypes = [ctypes.c_void_p]
    public = crypto.EVP_PKEY_new_raw_public_key_ex(None, b"ED25519", None, key, len(key))
    context = crypto.EVP_MD_CTX_new()
    try:
        if not public or not context or crypto.EVP_DigestVerifyInit(
                context, None, None, None, public) != 1 or crypto.EVP_DigestVerify(
                    context, signature, len(signature), payload, len(payload)) != 1:
            raise ValueError("Подпись реестра не прошла проверку.")
    finally:
        if context:
            crypto.EVP_MD_CTX_free(context)
        if public:
            crypto.EVP_PKEY_free(public)


def https_url(url):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password or parts.fragment:
        raise ValueError("Для реестра и пакетов требуется HTTPS URL.")
    return url


class HttpsRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, url):
        https_url(url)
        return super().redirect_request(request, response, code, message, headers, url)


def download(url, limit):
    https_url(url)
    request = urllib.request.Request(url, headers={"User-Agent": "Ovygram-PluginRegistry/1"})
    with urllib.request.build_opener(HttpsRedirect()).open(request, timeout=15) as response:
        https_url(response.geturl())
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Ответ сервера превышает допустимый размер.")
    return data


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Повторяющееся поле JSON.")
        result[key] = value
    return result


def json_document(payload):
    document = json.loads(payload, object_pairs_hook=unique_object,
                          parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    if not isinstance(document, dict):
        raise ValueError("Ожидается объект JSON.")
    return document


def unavailable(reason=UNAVAILABLE):
    return {"status": "verification_unavailable", "reason": reason,
            "chain": None, "release_sequence": None}


class Registry:
    def __init__(self, config=None, fetch=download, now=None):
        if config is None:
            path = Path(__file__).with_name("registry.json")
            config = json_document(path.read_bytes()) if path.exists() else {}
            config = {**config,
                      "server_url": os.environ.get("OVYGRAM_REGISTRY_URL") or config.get("server_url", ""),
                      "index_url": os.environ.get("OVYGRAM_PLUGIN_INDEX_URL") or config.get("index_url", "")}
        self.url = config.get("server_url", "").rstrip("/")
        self.index_url = config.get("index_url", "")
        self.keys = config.get("public_keys", {})
        self.fetch = fetch
        self.now = now or (lambda: datetime.now(timezone.utc))

    def validate(self, answer):
        key = base64.b64decode(self.keys[answer["key_id"]], validate=True)
        if hashlib.sha256(key).hexdigest()[:16] != answer["key_id"]:
            raise ValueError("ID ключа не совпадает с закреплённым ключом.")
        verify_ed25519(key, base64.b64decode(answer["signature"], validate=True), canonical(answer))
        issued = datetime.fromisoformat(answer["issued_at"].replace("Z", "+00:00"))
        expires = datetime.fromisoformat(answer["expires_at"].replace("Z", "+00:00"))
        now = self.now()
        if issued.tzinfo is None or expires.tzinfo is None or not issued <= now < expires \
                or (expires - issued).total_seconds() > 8 * 86400:
            raise ValueError("Ответ реестра устарел или имеет некорректное время.")
        return answer

    def signed(self, path):
        if not self.url or not self.keys:
            raise ValueError("Реестр не настроен: требуются URL и закреплённый публичный ключ.")
        return self.validate(json_document(self.fetch(self.url + path, 2 * 1024 * 1024)))

    def match(self, answer, metadata, digest, kind):
        if (answer.get("plugin_id"), answer.get("sha256"), answer.get("package_type")) != (
                metadata["id"], digest, kind) or answer.get("status") not in STATUSES:
            raise ValueError("Ответ реестра относится к другому файлу.")
        if answer["status"] in TRUSTED:
            if answer.get("version") != metadata["version"] \
                    or answer.get("release") is not metadata["release"] \
                    or type(answer.get("chain")) is not int or answer["chain"] < 1 \
                    or type(answer.get("release_sequence")) is not int or answer["release_sequence"] < 1:
                raise ValueError("Подтверждённые метаданные не совпадают с пакетом.")
            if answer["status"] == "official" and metadata["author"] != "Ovygram":
                raise ValueError("Некорректное подтверждение официального автора.")
        return answer

    def check(self, metadata, digest, kind):
        try:
            query = urllib.parse.urlencode({"plugin_id": metadata["id"], "sha256": digest,
                                            "package_type": kind})
            return self.match(self.signed("/v1/check?" + query), metadata, digest, kind)
        except Exception as error:
            return unavailable(str(error))

    def cached(self, version):
        if version.get("verification_unavailable") and not version.get("blocked"):
            return unavailable()
        answer = version.get("trust", {})
        try:
            return self.match(self.validate(answer), version["metadata"], version["sha256"],
                              version["package_type"])
        except Exception:
            # An outage/expiry must never remove a known block.
            return {**unavailable(), "status": "blocked"} if version.get("blocked") else unavailable()

    def index(self):
        if not self.index_url:
            return {}
        result = json_document(self.fetch(https_url(self.index_url), 2 * 1024 * 1024))["plugins"]
        if not isinstance(result, dict):
            raise ValueError("Некорректный индекс плагинов.")
        return result

    def chain(self, chain, plugin_id):
        answer = self.signed(f"/v1/chains/{int(chain)}")
        if answer.get("chain") != chain or answer.get("plugin_id") != plugin_id \
                or not isinstance(answer.get("versions"), list):
            raise ValueError("Ответ относится к другой цепочке автора.")
        return answer["versions"]

    def info(self, url, plugin_id):
        # Discovery only: every selected package still needs a signed check.
        answer = json_document(self.fetch(https_url(url), 2 * 1024 * 1024))
        if answer.get("id") != plugin_id or not isinstance(answer.get("versions"), list):
            raise ValueError("Карточка версий относится к другому плагину.")
        return answer["versions"]

    def package(self, url):
        return self.fetch(https_url(url), MAX_PACKAGE)


CONFUSABLES = str.maketrans({"о": "o", "ο": "o", "ѵ": "v", "у": "y", "ү": "y",
                            "ɡ": "g", "ԍ": "g", "г": "r", "а": "a", "α": "a",
                            "м": "m", "ｍ": "m", "0": "o"})


def protected_author(author, status):
    if status in TRUSTED:
        return False
    normalized = unicodedata.normalize("NFKC", author).casefold().translate(CONFUSABLES)
    normalized = "".join(character for character in normalized
                         if unicodedata.category(character)[0] not in ("C", "M"))
    if "ovygram" in normalized:
        return True
    for word in re.findall(r"[^\W_]+", normalized):
        if not 5 <= len(word) <= 9:
            continue
        row = list(range(8))
        for index, character in enumerate(word, 1):
            current = [index]
            for column, expected in enumerate("ovygram", 1):
                current.append(min(current[-1] + 1, row[column] + 1,
                                   row[column - 1] + (character != expected)))
            row = current
        if row[-1] <= 2:
            return True
    return False
