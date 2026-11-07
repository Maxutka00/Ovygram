param(
    [Parameter(Mandatory)] [string] $Source,
    [Parameter(Mandatory)] [string] $PythonRoot
)

$ErrorActionPreference = 'Stop'
$pluginHostCompile = @(
    '/nologo', '/std:c++20', '/EHsc', '/utf-8', '/MTd', '/D_DEBUG',
    "/I$Source/Telegram/SourceFiles",
    "/I$PythonRoot/tools/include",
    "/I$PythonRoot/pybind11/include",
    "$Source/Telegram/SourceFiles/core/plugin_runtime.cpp",
    "$Source/Telegram/SourceFiles/core/plugin_runtime_exports.cpp",
    '/LD', '/Fe:python/ovygram_host.dll', '/link',
    '/DEPENDENTLOADFLAG:0', '/IMPLIB:plugin_host_smoke.lib',
    "/LIBPATH:$PythonRoot/tools/libs", 'python313.lib'
)
$pluginClientCompile = @(
    '/nologo', '/std:c++20', '/EHsc', '/utf-8', '/MTd', '/D_DEBUG',
    "/I$Source/Telegram/SourceFiles",
    "$Source/Telegram/SourceFiles/core/plugin_runtime_bridge.cpp",
    "$Source/tools/ovygram/plugin_host_smoke.cpp",
    '/Fe:plugin_host_smoke.exe', '/link', '/DEPENDENTLOADFLAG:0x800'
)
Push-Location -LiteralPath $PythonRoot
try {
    & cl.exe @pluginHostCompile
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & cl.exe @pluginClientCompile
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $env:OVYGRAM_SMOKE_EXE = Join-Path $PythonRoot 'plugin_host_smoke.exe'
    python -m unittest discover -s "$Source/tools/ovygram/tests" -p test_plugin_runtime.py -v
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    # The smoke host is a debug build: keep it out of the staged bundle.
    Remove-Item -LiteralPath 'python/ovygram_host.dll' -ErrorAction SilentlyContinue
    Pop-Location
}
