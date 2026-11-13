from dataclasses import dataclass
from collections.abc import Callable


@dataclass(frozen=True)
class Header:
    text: str


@dataclass(frozen=True)
class Button:
    key: str
    text: str
    on_click: Callable[[], object]


@dataclass(frozen=True)
class Switch:
    key: str
    text: str
    default: bool = False


@dataclass(frozen=True)
class Input:
    key: str
    text: str
    default: str = ""


@dataclass(frozen=True)
class Selector:
    key: str
    text: str
    items: list[str]
    default: int = 0
