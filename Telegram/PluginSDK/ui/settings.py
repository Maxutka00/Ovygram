from dataclasses import dataclass


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
