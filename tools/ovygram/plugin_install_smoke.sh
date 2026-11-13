#!/bin/sh
# Compile the production C++ installer against standalone Qt, with a fixture
# for the host boundary. Requires Qt6Widgets development files and pkg-config.
# Usage: plugin_install_smoke.sh <output directory>
set -eu
output=$(realpath "$1")
source=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
fixture="$source/tools/ovygram/tests/native_install"
g++ -std=c++20 -fPIC -include "$fixture/prelude.h" \
    -I"$fixture" -I"$source/Telegram/SourceFiles" \
    $(pkg-config --cflags Qt6Widgets) \
    "$source/Telegram/SourceFiles/ovygram/plugin_install.cpp" "$fixture/main.cpp" \
    -o "$output/plugin_install_smoke" $(pkg-config --libs Qt6Widgets)
for mode in offline loss verified blocked; do
    QT_QPA_PLATFORM=offscreen "$output/plugin_install_smoke" "$mode" "$output/$mode.png"
done
