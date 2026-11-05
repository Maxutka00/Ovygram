import ast
from pathlib import Path
import sys

from dependency_cache import group_for


def grouped_recipe(text, filename, group):
    tree = ast.parse(text, filename=filename)
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef) and node.name == 'runStages']
    if len(functions) != 1:
        raise RuntimeError('Pinned prepare recipe no longer has exactly one runStages.')
    selection = ast.parse(
        "stages[:] = [entry for entry in stages if "
        f"_desktop_group_for(entry['name']) == {group!r}]").body[0]
    functions[0].body.insert(0, selection)
    return compile(ast.fix_missing_locations(tree), filename, 'exec')


def main():
    group, filename = sys.argv[1:3]
    if group not in ('foundation', 'qt', 'extras'):
        raise ValueError('Unknown dependency group.')
    recipe = Path(filename).resolve()
    sys.path.insert(0, str(recipe.parent))
    sys.argv = [str(recipe), 'qt6', 'skip-release', 'silent']
    namespace = {'__file__': str(recipe), '__name__': '__main__',
                 '_desktop_group_for': group_for}
    exec(grouped_recipe(recipe.read_text(encoding='utf-8'), str(recipe), group), namespace)


if __name__ == '__main__':
    main()
