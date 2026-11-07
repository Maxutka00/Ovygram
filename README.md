# Ovygram

Ovygram is an unofficial fork of [Telegram Desktop](https://github.com/telegramdesktop/tdesktop)
for Windows x64 and Linux x64 with an embedded Python runtime and a plugin SDK.
It is based on Telegram Desktop **v7.3.5** and targets Windows 11 and Linux.

Plugins are managed from the client's settings, with support for import,
configuration, and rollback. The SDK covers accounts, messages, history, files,
events, and Telegram RPC hooks. Plugins run in the client process.

SDK 2 is in development. Its Python tests pass, and validation of the Windows
client is pending. Linux support is new and is also still being validated.

## Building

The client is built with CMake through `Telegram/configure.py`. The configuration
always needs your own [API credentials](docs/api_credentials.md), and plugin
support needs a Python bundle prepared by `tools/ovygram/python_bundle.py`.
Without `OVYGRAM_PYTHON_ROOT`, the client is built without plugins.

- **Windows x64:** follow the [Windows build guide](docs/building-ovygram.md).
- **Linux x64:** follow the steps below.

### Linux

These steps build against system libraries on Arch Linux, which is suitable for
local use. To distribute a build, use the Docker image from
[building-linux.md](docs/building-linux.md) and prepare the Python bundle inside
it, because binaries built on Arch require an equally new glibc.

1. Get the submodules:

   ```sh
   git submodule update --init --recursive
   ```

2. Install the [required packages](docs/building-ovygram.md#packages), and build
   [`tde2e` and `wallet-engine`](docs/building-ovygram.md#libraries-outside-the-repositories),
   which are not in the Arch repositories.

3. Build the pinned CPython and stage it with pybind11 and the SDK:

   ```sh
   python3 tools/ovygram/python_bundle.py --root ../plugin-python --downloads ../python-downloads --sdk Telegram/PluginSDK
   ```

4. Configure, using absolute paths:

   ```sh
   python3 Telegram/configure.py \
       -D BUILD_EMBED_IGNORE=ON \
       -D OVYGRAM_PYTHON_ROOT=/abs/path/plugin-python \
       -D tde2e_DIR=/abs/path/deps/tde2e/install/lib/cmake/tde2e \
       -D CMAKE_PREFIX_PATH=/abs/path/deps/wallet-engine/install \
       -D TDESKTOP_API_ID=YOUR_API_ID \
       -D TDESKTOP_API_HASH=YOUR_API_HASH
   ```

5. Build outside any Python virtual environment, because `g-ir-scanner` fails
   with `No module named 'distutils'` inside one. Choose `-j` by available
   memory:

   ```sh
   cmake --build out --config Release --target Telegram -j 4
   ```

The result is `out/Release/Telegram`, with its Python runtime in
`out/Release/python`.

To link the system Python 3.13 or newer instead of building CPython, add
`--system-python` in step 3 and `-D OVYGRAM_SYSTEM_PYTHON=ON` in step 4. Such a
build is tied to the Python version it was built against. See the
[Linux build guide](docs/building-ovygram.md#linux-x64) for details.

## Documentation

- [Plugin manager](docs/plugins.md)
- [Plugin SDK](docs/sdk.md)
- [Example plugins](tools/ovygram/examples)
- [Windows and Linux build guide](docs/building-ovygram.md)
- [Development status](docs/development-status.md)

## License

Ovygram is licensed under the GNU General Public License, version 3 or later,
with the upstream OpenSSL linking exception. Third-party components retain
their own licenses. See [LICENSE](LICENSE), [LEGAL](LEGAL), [NOTICE](NOTICE),
and the [upstream README](README.upstream.md).
