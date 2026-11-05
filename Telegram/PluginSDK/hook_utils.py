"""Ordered plugin hooks. Modifications are committed after validation."""

from dataclasses import dataclass
from enum import Enum


class HookStrategy(Enum):
    DEFAULT = "default"
    CANCEL = "cancel"
    MODIFY = "modify"
    MODIFY_FINAL = "modify_final"


DEFAULT = HookStrategy.DEFAULT
CANCEL = HookStrategy.CANCEL
MODIFY = HookStrategy.MODIFY
MODIFY_FINAL = HookStrategy.MODIFY_FINAL


@dataclass(frozen=True)
class HookResult:
    strategy: HookStrategy = DEFAULT
    value: object = None
    reason: str = ""


class HookError(RuntimeError):
    pass


class HookCancelled(HookError):
    pass
