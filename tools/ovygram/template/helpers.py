"""Code split out of main.py: modules of a ZIP plugin import each other
relatively, e.g. "from .helpers import greeting"."""


def greeting(name, excited):
    return f"Привет, {name}{'!' if excited else '.'}"
