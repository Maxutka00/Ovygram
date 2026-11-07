#!/bin/sh
# Linux counterpart of plugin_host_smoke.ps1.
# Usage: plugin_host_smoke.sh <source root> <python bundle root>
set -eu
source=$(realpath "$1")
root=$(realpath "$2")
cd "$root"
g++ -std=c++20 -shared -fPIC -fvisibility=hidden -fvisibility-inlines-hidden \
    -I"$source/Telegram/SourceFiles" \
    -isystem tools/include -isystem pybind11/include \
    "$source/Telegram/SourceFiles/core/plugin_runtime.cpp" \
    "$source/Telegram/SourceFiles/core/plugin_runtime_exports.cpp" \
    -o python/ovygram_host.so \
    tools/libs/libpython3.13.so -Wl,-rpath,'$ORIGIN'
g++ -std=c++20 -I"$source/Telegram/SourceFiles" \
    "$source/Telegram/SourceFiles/core/plugin_runtime_bridge.cpp" \
    "$source/tools/ovygram/plugin_host_smoke.cpp" \
    -o plugin_host_smoke -ldl
OVYGRAM_SMOKE_EXE="$root/plugin_host_smoke" python3 -m unittest discover \
    -s "$source/tools/ovygram/tests" -p test_plugin_runtime.py -v
