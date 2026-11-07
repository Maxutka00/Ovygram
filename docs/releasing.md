# Releasing Ovygram

A release is tagged `v<ovygram>-<telegram>`, e.g. `v0.1.0-7.3.5`, and ships
the sources with these assets:

| Asset | Made by |
| --- | --- |
| `Ovygram-win64-portable.zip` | GitHub Actions, `ovygram-windows.yml` in `plugins` mode |
| `ovygram-<version>-linux-x86_64.tar.xz` and `.sha256` | `tools/ovygram/package_linux.py` on Arch Linux |

The versions are `OVYGRAM_VERSION` and `CLIENT_VERSION` in
`tools/ovygram/baseline.py`; the About box shows the same version.

Auto-update from the official Telegram channel is off in every build
(`DESKTOP_APP_DISABLE_AUTOUPDATE`), so an official update never replaces
the fork. Users update by installing the new version over the old one; the
data directory stays.

## Linux

The Linux build links the system libraries of the machine it is built on
(Qt 6, FFmpeg and the others from the Arch repositories), so the archive is
meant for Arch Linux and the `ovygram-bin` package.

1. Stage the Python bundle (`tools/ovygram/python_bundle.py`, it includes
   the pip wheel) and build Release as in
   [building-ovygram.md](building-ovygram.md#linux-x64).
2. Pack: `python tools/ovygram/package_linux.py --build out/Release`. The
   script refuses a `python` directory without `pip.whl` or the current SDK,
   strips the binary and writes the archive and its `.sha256` to `dist/`.
3. If the build machine's libraries changed, refresh the dependencies:
   `python tools/ovygram/arch_depends.py out/Release` and update `depends`
   in `packaging/arch/ovygram-bin/PKGBUILD` (keep the runtime-only ones:
   `hicolor-icon-theme`, `pipewire`, `qt6-imageformats`).

The application ID is `io.github.maxutka00.Ovygram`: the `.desktop` file,
the icons, the Wayland app ID and the D-Bus name. Ovygram keeps its data in
`~/.local/share/Ovygram` and never reads `~/.TelegramDesktop`, so it runs
next to the official Telegram Desktop.

## Windows

Run `ovygram-windows.yml` with `mode: plugins` on the commit being released
and take `Ovygram-win64-portable.zip` from the run artifacts. Check it on
Windows 11 without Python installed.

## Publishing

1. Go through [the client checklist](ui-checklist.md) on both systems.
2. Tag and publish (the notes are in `docs/release-notes/`):

   ```
   git tag -a v0.1.0-7.3.5 -m "Ovygram 0.1.0 (Telegram Desktop 7.3.5)"
   git push origin v0.1.0-7.3.5
   gh release create v0.1.0-7.3.5 --notes-file docs/release-notes/0.1.0-7.3.5.md \
       dist/ovygram-0.1.0-7.3.5-linux-x86_64.tar.xz \
       dist/ovygram-0.1.0-7.3.5-linux-x86_64.tar.xz.sha256 \
       Ovygram-win64-portable.zip
   ```

3. AUR: in `packaging/arch/ovygram-bin`, put the archive's SHA-256 into
   `sha256sums` (or run `updpkgsums`), check with `makepkg -f`, regenerate
   `.SRCINFO` with `makepkg --printsrcinfo > .SRCINFO` and push both files to
   `ssh://aur@aur.archlinux.org/ovygram-bin.git`.

Before a public release the application also needs its own API credentials
and icon, see [development-status.md](development-status.md).
