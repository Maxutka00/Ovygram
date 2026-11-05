$ErrorActionPreference = 'Stop'
$taskRoot = $env:GITHUB_WORKSPACE
if (-not $taskRoot) { throw 'Run this script in the baseline GitHub Actions workflow.' }
$taskReport = Join-Path $taskRoot 'reports/toolchain.json'
$taskVswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio/Installer/vswhere.exe'
$taskState = [ordered]@{
    image = $env:ImageOS
    image_version = $env:ImageVersion
    status = 'checking'
    error = $null
}
try {
    if (-not (Test-Path -LiteralPath $taskVswhere)) { throw 'Visual Studio Installer is missing.' }
    $taskVs = & $taskVswhere -latest -products '*' -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
    if ($LASTEXITCODE -ne 0 -or -not $taskVs) { throw 'MSVC x64 tools are missing.' }
    $taskState.visual_studio = $taskVs
    $taskDevShell = Join-Path $taskVs 'Common7/Tools/Microsoft.VisualStudio.DevShell.dll'
    Import-Module $taskDevShell
    Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x64 -host_arch=x64 -vcvars_ver=14.44 -winsdk=10.0.26100.0'
    if (-not $env:VCToolsVersion.StartsWith('14.44.')) { throw 'Required MSVC 14.44 toolset is missing.' }
    if ($env:WindowsSDKVersion.TrimEnd('\') -ne '10.0.26100.0') { throw 'Required Windows SDK 10.0.26100.0 is missing.' }
    if ($env:VSCMD_ARG_TGT_ARCH -ne 'x64') { throw 'Expected an x64 compiler environment.' }
    $env:Platform = 'x64'
    $taskState.platform = $env:Platform
    if ($env:VisualStudioVersion -notmatch '^18\.') { throw 'Expected VisualStudioVersion for VS 2026.' }
    $taskState.visual_studio_version = $env:VisualStudioVersion
    $taskState.msvc = $env:VCToolsVersion
    $taskState.sdk = $env:WindowsSDKVersion
    foreach ($taskTool in @('python','cmake','ninja','git','cl')) {
        $taskState[$taskTool] = (Get-Command $taskTool -ErrorAction Stop).Source
    }
    $taskState.python_version = (& python --version)
    $taskState.cmake_version = (& cmake --version | Select-Object -First 1)
    $taskState.status = 'ready'
    Get-ChildItem Env: | Where-Object {
        $_.Name -match '^(PATH|INCLUDE|LIB|LIBPATH|Platform|VisualStudioVersion|VSCMD_.*|VSINSTALLDIR|VCINSTALLDIR|VCTools.*|WindowsSDK.*|WindowsSdk.*|UniversalCRTSdkDir|UCRTVersion|ExtensionSdkDir|DevEnvDir)$'
    } | ForEach-Object {
        Add-Content -LiteralPath $env:GITHUB_ENV -Value "$($_.Name)=$($_.Value)" -Encoding utf8
    }
} catch {
    $taskState.status = 'blocked'
    $taskState.error = $_.Exception.Message
    throw
} finally {
    $taskState | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $taskReport -Encoding utf8NoBOM
}
