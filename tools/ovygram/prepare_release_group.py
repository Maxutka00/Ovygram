"""Prepare pinned Windows dependencies for the optimized client."""
from pathlib import Path
import sys

from dependency_cache import group_for
from prepare_group import grouped_recipe


def release_recipe(text, filename, group):
    if group == 'foundation':
        # The portable bundle has no symbol upload step. Keep the Breakpad
        # client libraries, but skip dump_syms, which requires the ATL SDK.
        dump_syms = (
            '    cd tools\\\\windows\\\\dump_syms\n'
            '    gyp dump_syms.gyp --format=msvs\n'
            '    msbuild -m dump_syms.vcxproj /property:Configuration=Release '
            '/property:Platform="x64" %ToolsetProp%\n')
        if text.count(dump_syms) != 1:
            raise RuntimeError('Pinned Breakpad recipe changed. Review the symbol tool step.')
        text = text.replace(dump_syms, '')
    elif group == 'qt':
        # Preserve upstream's patching and flags. Build only the variant we link
        # and omit the extra Qt debug symbols to stay within runner disk limits.
        changes = {
            'SET CONFIGURATIONS=-debug-and-release': 'SET CONFIGURATIONS=-release',
            '        -force-debug-info ^\n': '',
            ('    cmake --build . --config Debug\n'
             '    cmake --install . --config Debug\n'
             '    cmake --build .\n'
             '    cmake --install .\n'): ('    cmake --build . --config Release\n'
                                          '    cmake --install . --config Release\n'),
        }
        marker = "else: # qt > '6'\n"
        head, separator, qt = text.partition(marker)
        if not separator or any(qt.count(original) != 1 for original in changes):
            raise RuntimeError('Pinned Qt recipe changed. Review the Release-only configuration.')
        for original, updated in changes.items():
            qt = qt.replace(original, updated)
        text = head + separator + qt
    return grouped_recipe(text, filename, group)


def main():
    group, filename = sys.argv[1:3]
    if group not in ('foundation', 'qt', 'extras'):
        raise ValueError('Unknown dependency group.')
    recipe = Path(filename).resolve()
    sys.path.insert(0, str(recipe.parent))
    sys.argv = [str(recipe), 'qt6', 'silent']
    namespace = {'__file__': str(recipe), '__name__': '__main__',
                 '_desktop_group_for': group_for}
    exec(release_recipe(recipe.read_text(encoding='utf-8'), str(recipe), group), namespace)


if __name__ == '__main__':
    main()
