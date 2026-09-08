"""Print the Scene classes defined in a manim file, in source order.

Usage (via ./render.sh list <file.py>):
    python tools/list_scenes.py _2016/eola/chapter1.py
"""
import ast
import sys


def class_line_numbers(path):
    """Map class name -> line number by parsing the file (import machinery
    used by manimlib hides the source from `inspect`)."""
    with open(path, encoding="utf-8") as fp:
        tree = ast.parse(fp.read(), filename=path)
    return {
        node.name: node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    }


def main():
    if len(sys.argv) < 2:
        print("usage: list_scenes.py <file.py>", file=sys.stderr)
        return 1
    target = sys.argv[1]

    # manimlib parses sys.argv at import time, so make it look like a plain run
    sys.argv = ["manimgl", target]
    from manimlib.extract_scene import get_scene_classes
    from manimlib.module_loader import ModuleLoader

    module = ModuleLoader.get_module(target, False)
    names = [cls.__name__ for cls in get_scene_classes(module)]
    lines = class_line_numbers(target)

    for name in sorted(names, key=lambda n: lines.get(n, 10**9)):
        print(f"{lines.get(name, 0):>6}  {name}")
    print(f"\n총 {len(names)}개 씬  ({target})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
