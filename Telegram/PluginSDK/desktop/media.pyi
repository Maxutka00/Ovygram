from collections.abc import Callable
from pathlib import Path
from typing import Any
from . import tl
from .models import Attachment, Chat, Progress

async def send_file(chat: Chat, path: str | Path, *, caption: str = "", progress: Callable[[Progress], Any] | None = None, silent: bool = False) -> tl.TLObject: ...
async def download_file(attachment: Attachment, destination: str | Path, *, progress: Callable[[Progress], Any] | None = None) -> Path: ...
