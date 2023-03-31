from os import PathLike
from pathlib import Path

from .fs import BaseFS

__all__ = ['LocalFS']


class LocalFS(BaseFS):
    def __init__(self, root: str | PathLike) -> None:
        self._root = Path(root)

    def read_file(self, path: str | PathLike) -> bytes | None:
        file = self._root / path
        if not file.exists():
            return None
        assert file.is_file
        return file.read_bytes()

    def write_file(self, path: str | PathLike, content: bytes) -> int:
        file = self._root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        return file.write_bytes(content)
