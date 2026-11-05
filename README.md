# Ovygram

Ovygram is an unofficial fork of [Telegram Desktop](https://github.com/telegramdesktop/tdesktop)
for Windows x64 with an embedded Python runtime and a plugin SDK. It is based on
Telegram Desktop **v7.3.5** and targets Windows 11.

Plugins are managed from the client's settings, with support for import,
configuration, and rollback. The SDK covers accounts, messages, history, files,
events, and Telegram RPC hooks. Plugins run in the client process.

SDK 2 is in development. Its Python tests pass, and validation of the Windows
client is pending.

## Documentation

- [Plugin manager](docs/plugins.md)
- [Plugin SDK](docs/sdk.md)
- [Example plugins](tools/ovygram/examples)
- [Windows build guide](docs/building-ovygram.md)
- [Development status](docs/development-status.md)

## License

Ovygram is licensed under the GNU General Public License, version 3 or later,
with the upstream OpenSSL linking exception. Third-party components retain
their own licenses. See [LICENSE](LICENSE), [LEGAL](LEGAL), [NOTICE](NOTICE),
and the [upstream README](README.upstream.md).
