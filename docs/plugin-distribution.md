# Plugin installation, trust and updates

The shared parser is `Telegram/PluginSDK/ovygram_package.py`. Distribution
uses `.ovyplugin` and `.ovyzip`; local import also accepts `.py`, `.plugin`
and `.zip`. Metadata is read without running the package. `__desktop_sdk__`
is the minimum Desktop SDK required: an integer from 1 through the client's
`SDK_VERSION` (currently 2). A higher value is incompatible and is refused.

## Registry configuration

`Telegram/PluginSDK/registry.json` already pins the generated Ed25519 public
key `543138e5eaa5851c`. Its `server_url` and `index_url` are intentionally
empty until deployment. Set the real HTTPS API and GitHub index URLs before
shipping a connected build. Nonempty `OVYGRAM_REGISTRY_URL` and
`OVYGRAM_PLUGIN_INDEX_URL` environment variables override these endpoints;
they do not replace the pinned public keys. Explicit `Registry(config)`
configuration takes precedence over environment variables.
The bundle script and CMake copy that directory into `python/sdk`.
These values are public deployment configuration, never API tokens or private
keys. The HTTPS server must expose `/v1/check` and `/v1/chains/{chain}`.

`public_keys` maps the first 16 hexadecimal characters of SHA-256 of a raw
32-byte Ed25519 public key to its base64 value. Pin keys through a trusted
release process. The client never trusts a key downloaded from `/v1/keys`.
To rotate keys, distribute a build containing both keys before switching the
server signer. OpenSSL 3 libcrypto performs verification; Windows uses the
DLL next to the bundled Python executable, Linux uses the system library.

Without a configured registry, or on invalid signatures, expired responses,
network errors or mismatched package metadata, the client shows verification
unavailable. A manual install then needs an additional confirmation.
No automatic update can proceed in that state. Known blocks survive outages
and expired responses. A failed refresh hides a previous green/blue badge
while retaining the confirmed chain for a later retry.

## Installation and trust

Import from Settings → Plugins or open a downloaded `.ovyplugin`/`.ovyzip`
in a chat. A native C++ application-modal dialog shows the complete metadata,
safe author display, exact SHA-256 and server status. Package-provided text
uses plain text. Cancel is the default button, including on warnings.
`blocked` cannot be installed or enabled. An unconfirmed author resembling
Ovygram, including common Cyrillic/Greek lookalikes and invisible characters,
is displayed as “Неизвестный автор”. Only the exact `Ovygram` author with a
valid `official` server confirmation receives the official badge.

Preparation reads, hashes and checks a package in a background worker.
The installer retains those bytes, so a change to the selected path between
preview and confirmation cannot replace the payload. On ID collisions, the
dialog shows both sets of full metadata and offers updates of the individual
installations. Two trusted instances cannot be installed alongside each
other. A separate unverified instance gets independent settings and data.
Replacing a trusted version with an unconfirmed version needs a separate
warning and leaves the new code disabled. Trust is never inherited.

While the dialog is open, the C++ plugin boundary refuses widget, native,
compose, UI creation and run-on-UI commands; native/widget event filters and
client hooks do not expose its controls. The installer is outside the Plugin
API surface tree. This protects the supported SDK boundary; plugins still run
arbitrary Python in the application process. It is **not a process sandbox**
against direct ctypes/Qt/process access or monkey-patching Python internals.

## Checks, updates and recovery

The host timer polls worker results on the main thread. On startup and at
subsequent half-day boundaries, it starts one check per local calendar date
and half-day, persisted across restarts. “Проверить обновления” bypasses the
schedule. Network I/O happens outside the UI thread.

Every check refreshes installed file statuses independently of GitHub
availability. `blocked` disables the installation and prevents re-enabling;
`revoked` removes trust and notifies without automatically disabling it.
The client offers a previously approved version from the same author chain,
using the saved local package or a published URL from the signed chain API.
The rollback target is checked again when requested, including its SHA-256.

The GitHub index only discovers update candidates. A user requests an update
from the installation's details page; the client downloads once, checks the
actual hash and signed tuple, chain, release flag, sequence, version and SDK.
Only a higher `release_sequence` can update a confirmed public installation.
An installed `release: false` or unverified file does not automatically join
a public chain. A manual file update can make that transition.

Updates keep the installation UUID, settings and data. The previous package
is retained. If activation of an enabled plugin fails, code and settings
are restored and the previous version is loaded, unless a failing unload
requires restarting the application. Extracted source/resource files are
checked against the original package before execution; extra executable
modules, bytecode and symlinks are rejected. Local state writes are atomic.

Deletion offers to retain settings and data. Retained settings are saved
under `plugins/retained/<installation_id>/settings.json`; data stays under
`plugins/data/<installation_id>`. A new installation does not inherit them.

## Validation

Run the SDK suite on the pinned CPython 3.13.16. With a built host, set
`OVYGRAM_SMOKE_EXE` as in `tools/ovygram/plugin_host_smoke.sh`.
The distribution tests use real Ed25519 signatures and controlled transport.
The server suite also tests its signed answers against this SDK when both
repositories are checked out side by side.

To compile and exercise the production native dialog independently, install
Qt6Widgets development files, create an output directory and run:

```sh
sh tools/ovygram/plugin_install_smoke.sh /absolute/output/directory
```

This verifies native dialog behavior using a fixture host boundary and saves
screenshots for unavailable verification, trust loss, a trusted duplicate
and a blocked file. It does not replace a full Telegram build and testing
with an authenticated Telegram session on Linux and Windows.

## Дополнение после повторной сверки

Для установки обновления теперь требуется подписанное сервером
`publication = published` и опубликованный URL целевого пакета. Если последняя
версия требует более новый Desktop SDK, клиент читает `info_url` и проверяет
предыдущие кандидаты по убыванию последовательности, не опускаясь до уже
установленной версии. Каждому кандидату всё равно нужна проверка точных байтов,
цепочки автора и публикации. Другие ошибки проверки не превращаются в
разрешение обновления.

Незавершённые обновления записываются в `pending_updates` до замены кода.
До запуска плагинов при следующем старте восстанавливаются прежняя запись
экземпляра и настройки. Аварийный маркер по-прежнему требует обычного
подтверждения возобновления плагинов. Восстановление после принудительного
выхода Python-процесса проверяется отдельным тестом.

Владелец отложил полную защиту собственных системных окон и вкладок от
намеренного обхода SDK на будущую итерацию. Текущая архитектура не даёт этой
гарантии; TODO описан в [protected-ui-architecture.md](protected-ui-architecture.md)
и `ovygram-info/ideas/protected-system-ui.md`. Переход к изолированным процессам
сейчас не выполняется. Отдельная модель разрешений не входит в текущий объём:
настройки, данные и обработчики принадлежат `installation_id`.

Пара Ed25519 создана через `cryptography` и случайность ОС. Закрытый ключ
хранится отдельно от клиента в игнорируемом Git файле
`Ovygram-main-repo/secrets/signing.key`; публичные сведения —
`Ovygram-main-repo/registry-public-key.json`. Перенос и подключение описаны
в `Ovygram-main-repo/docs/signing-keys.md`. Не генерируйте новый ключ при
обычной сборке или переносе сервера.
