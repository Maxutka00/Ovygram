# Building Ovygram for Windows and Linux x64

Most of this document applies to Windows; the Linux differences are in the
[Linux x64](#linux-x64) section. This document describes the preparation for a
future build. The new SDK 2 version has not yet been compiled or validated in a
finished client.

## Tools and dependencies

The exact upstream tools are listed in [building-win.md](building-win.md).
Visual Studio 2026, MSVC 14.44 and Windows SDK 10.0.26100.0 are used. All
submodules are taken at pinned Git commits. Submodules must be initialized
recursively before preparing dependencies.

Working folder layout:

```text
D:\TBuild\
    tdesktop\         Ovygram sources
    ThirdParty\       upstream tools
    win64\Libraries\ Windows x64 dependencies
    plugin-python\    separate CPython and pybind11 bundle
    python-downloads\ downloaded Python archives
```

In a terminal with the MSVC x64 environment, prepare the dependencies with the
original `Telegram\build\prepare\win.bat`. For a consistent Release
configuration and compact caches, use the `tools/ovygram/baseline.py` stages
that the workflow relies on. A finished Ovygram.exe alone is not enough to
rebuild.

## Embedded Python

From `D:\TBuild\tdesktop`, prepare the bundle:

```powershell
python tools/ovygram/python_bundle.py --root D:/TBuild/plugin-python --downloads D:/TBuild/python-downloads --sdk Telegram/PluginSDK
```

The script verifies the SHA-256 of the CPython 3.13.16 and pybind11 3.0.2
archives. A separately installed Python is used only as a preparation tool;
users of the portable client do not need it.

## Configuration and compilation

From the source root, after preparing compatible Release dependencies:

```powershell
python Telegram/configure.py -G "Ninja Multi-Config" -D CMAKE_CONFIGURATION_TYPES=Release -D OVYGRAM_PYTHON_ROOT=D:/TBuild/plugin-python -D DESKTOP_APP_DISABLE_AUTOUPDATE=ON -D DESKTOP_APP_DISABLE_CRASH_REPORTS=ON -D TDESKTOP_API_ID=YOUR_API_ID -D TDESKTOP_API_HASH=YOUR_API_HASH
cmake --build out --config Release --target Telegram --parallel 2
```

`Telegram` remains the technical name of the upstream CMake target. The Windows
result is `out/Release/Ovygram.exe` with a `python` directory next to it.
Choose the number of parallel jobs by available memory. This is an example
command, not evidence of a successful build.

For test builds, the workflow uses `TDESKTOP_API_TEST=ON`; those credentials are
not intended for a public release of your own application. Do not add real keys
or profile directories to Git or public reports.

## Linux x64

The commands below target Arch Linux and a build against system libraries. Such
a client is meant for local use. To distribute a build, use the Docker image
from [building-linux.md](building-linux.md), because binaries built on Arch
require an equally new glibc. In that case, prepare the Python bundle inside the
image too.

### Packages

The list comes from the Arch `telegram-desktop` package recipe, extended with
the libraries needed to build CPython:

```sh
sudo pacman -S --needed base-devel cmake ninja git python just gperf \
    boost libtg_owt range-v3 tl-expected microsoft-gsl \
    qt6-base qt6-declarative qt6-imageformats qt6-svg qt6-wayland qt6-shadertools \
    vulkan-headers glib2 glib2-devel gobject-introspection \
    abseil-cpp ada cairo ffmpeg fontconfig hunspell kcoreaddons libavif libfido2 \
    libheif libjpeg-turbo libjxl libpipewire libsrtp libvpx libxcomposite libxdamage \
    libxkbcommon libxrandr libxtst lz4 minizip openal openh264 opus pango pipewire \
    rnnoise tlottie xxhash \
    openssl libffi sqlite zlib bzip2 xz
```

Rust with `cargo` is also required: either the `rust` package or `rustup` with
an installed toolchain. `boost-libs` is not enough, because the headers and
`BoostConfig.cmake` are only in `boost`.

### Libraries outside the repositories

`tde2e` and `wallet-engine` are not in the Arch repositories, so they are built
by hand from the revisions pinned in `Telegram/build/prepare/prepare.py`. The
working directory here is `../deps`, and the commands run from the source root:

```sh
mkdir -p ../deps && cd ../deps

git clone https://github.com/tdlib/td.git tde2e
cd tde2e && git checkout 51743df
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PWD/install" -DTD_E2E_ONLY=ON
cmake --build build && cmake --install build
cd ..

curl -fsSLO https://raw.githubusercontent.com/desktop-app/patches/a59fc82462fb2987e9f0ee1498e2db694410ae81/wallet-engine.patch
git clone https://github.com/i582/wallet-engine.git
cd wallet-engine
git checkout e59e0d89d7ee90c388bf36e3334c5b276f396697
git apply ../wallet-engine.patch
just build && just bindings-cpp
install -Dm644 target/release/libwallet_engine.a -t install/lib/
install -Dm644 bindings/cpp-experimental/* -t install/include/wallet_engine/
cd ../..
```

### Bundled Python

There are no official CPython binaries for Linux, so `python_bundle.py` builds
the pinned CPython 3.13.16 source archive. The system interpreter only runs the
script and does not end up in the client. A compiler, `make` and the development
packages of OpenSSL, libffi, SQLite, zlib, bzip2 and xz are required: if a module
depending on them fails to build, the script exits with an error.

```sh
python3 tools/ovygram/python_bundle.py --root ../plugin-python --downloads ../python-downloads --sdk Telegram/PluginSDK
```

### Linux configuration and compilation

Paths must be absolute. `BUILD_EMBED_IGNORE=ON` is required for CMake 4.4 and
newer, otherwise the `cppgir` submodule stops generation with an
`install-absolute-destination` error.

```sh
python3 Telegram/configure.py \
    -D BUILD_EMBED_IGNORE=ON \
    -D OVYGRAM_PYTHON_ROOT=/abs/path/plugin-python \
    -D tde2e_DIR=/abs/path/deps/tde2e/install/lib/cmake/tde2e \
    -D CMAKE_PREFIX_PATH=/abs/path/deps/wallet-engine/install \
    -D TDESKTOP_API_ID=YOUR_API_ID \
    -D TDESKTOP_API_HASH=YOUR_API_HASH
cmake --build out --config Release --target Telegram --parallel 4
```

Build outside any Python virtual environment: `g-ir-scanner` runs through
`python3` from `PATH`, and without `setuptools` in the environment it fails with
`No module named 'distutils'`. Choose the number of parallel jobs by available
memory.

A `python` directory with `ovygram_host.so`, `libpython3.13.so.1.0`,
`python313.zip` and the extension modules appears next to the binary. To check
the host and the interpreter without building the whole client:

```sh
tools/ovygram/plugin_host_smoke.sh . ../plugin-python
```

### System Python

Instead of building CPython, you can use a system Python 3.13 or newer. Prepare
the bundle with `--system-python` (it then contains only pybind11 and the SDK)
and add `-D OVYGRAM_SYSTEM_PYTHON=ON` to the configuration. The option is off by
default. Such a build is tied to the Python version of the system it was built
on, so it suits local use rather than distribution.

### Packaging

`tools/ovygram/package_linux.py --build out/Release` packs the build into a
`.tar.xz` for Arch Linux and the `ovygram-bin` package, see
[releasing.md](releasing.md#linux).

### System libraries

The `_ssl`, `_ctypes` and `_sqlite3` modules depend on the system OpenSSL, libffi
and SQLite, and the whole bundle depends on the glibc of the build machine. So
if the build is meant for other systems, prepare the bundle in the same
environment as the client.

## GitHub Actions

The `.github/workflows/ovygram-windows.yml` workflow runs only manually. Its
modes are `inspect`, `plugin-smoke`, `build` and `plugins`. Before running it,
check the free resources, allow Actions in the repository settings and confirm
`free_allowance_verified`. One attempt is limited to 345 minutes of scripts and
360 minutes of job time, the maximum job duration on a standard GitHub-hosted
runner. The remaining 15 minutes are for stopping processes, reporting and
uploading artifacts. Paid runners are not configured; increasing the attempt
time does not increase the account's free quotas.

For the `plugins` mode, keep `require_dependency_cache=true`: without a
compatible Release cache, the workflow stops before preparing the corresponding
dependency group. A Debug cache does not replace finished Release dependencies.
Preparing all dependencies from scratch and compiling the client can together
exceed 345 minutes, even if the compiler reports no errors.

If an attempt reached client compilation and stopped with
`Build time allowance exhausted`, check that the `foundation`, `qt` and `extras`
caches were saved successfully. Then start a new `plugins` run on the same branch
with `require_dependency_cache=true` and a confirmed `free_allowance_verified`.
Caches of one branch are not available to another working branch; use the branch
they were saved on. The client is compiled again, because its object files are
not cached.

Disable `require_dependency_cache` only for a separate attempt to prepare missing
caches, after checking the free resources. The time limit still applies; such an
attempt may manage to save the dependencies but not to build the client. Old
caches may not fit after a toolchain or recipe change.

The `plugins` mode builds Ovygram, and `build` builds the unchanged pinned
Telegram baseline. The future package names are `ovygram-0.1.0-7.4.3-win64-release.zip`
and `upstream-baseline-7.4.3-win64-debug.zip` respectively. There is no real new
ZIP at the moment; the history of earlier personal builds is not carried over to
this repository.
