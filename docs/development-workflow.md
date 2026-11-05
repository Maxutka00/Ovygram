# Ovygram development workflow

## Source and SDK checks

Use the existing checkout and inspect its branch and working tree before making
changes. Preserve the pinned upstream revision, submodules, and license notices.
Start with the [SDK documentation](sdk.md) and [development status](development-status.md).
Check changes with CPython 3.13 from the repository root.

```sh
python3.13 -B -m unittest discover -s tools/ovygram/tests -v
git diff --check
```

Record the test results and any skips. Native host validation requires the
Windows runtime from the build. Keep credentials and Telegram profile data
out of commits, logs, and issue reports. Use GitHub's noreply address for commits.

## Windows build and verification

Use the [Windows build guide](building-ovygram.md) for the toolchain and the
locked CPython and pybind11 versions. Use a separate Windows runner for native
compilation. The cloud checkout supports source changes and Python SDK checks.

Dispatch [the Windows workflow](../.github/workflows/ovygram-windows.yml) on
the branch that contains the reviewed changes. Use `plugins` for the client
and confirm `free_allowance_verified` after checking available free resources.
Use the standard Windows runner, the existing dependency caches, and the
240-minute script and 255-minute job limits. Stop and report disk or quota
limits. Record the run ID and commit, and check for an active run before
dispatching another one.

After a successful build, save the portable ZIP from Actions within one day.
Check its SHA-256, archive integrity, Windows x64 executable, and embedded
Python files. Validate the native host and SDK in a separate portable profile
on Windows. The owner signs in to Telegram for account-specific checks.

Public distributions use the project's Telegram API credentials and include
the corresponding source and build instructions. Follow the
[Telegram API terms](https://core.telegram.org/api/terms) and the repository's
[security reporting guide](../SECURITY.md).
