from collections.abc import Iterator
from os import PathLike
from pathlib import Path
from shutil import rmtree

from .fs import BaseFS

__all__ = ['BaseLocalFS', 'LocalFS']


class BaseLocalFS(BaseFS):
    def __init__(self, root: Path) -> None:
        self._root = root

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

    def remove(self, path: str | PathLike) -> None:
        file = self._root / path
        if not file.exists():
            return
        if file.is_dir():
            rmtree(file)
        else:
            file.unlink()

    def iter_dir(self, path: str | PathLike) -> Iterator[Path]:
        return Path(self._root / path).iterdir()

    def is_dir(self, path: str | PathLike) -> bool:
        return Path(self._root / path).is_dir()

    @property
    def root(self) -> Path:
        return self._root

    @property
    def is_ngit_repo(self) -> bool:
        return self._is_ngit_root(self._root)

    @staticmethod
    def _is_ngit_root(dir_: Path) -> bool:
        return (dir_ / '.ngit').is_dir()


class LocalFS(BaseLocalFS):
    def __init__(self) -> None:
        super().__init__(self._find_ngit_root())

    @staticmethod
    def _find_ngit_root() -> Path:
        cwd = Path.cwd()
        if LocalFS._is_ngit_root(cwd):
            return cwd
        for parent in cwd.parents:
            if LocalFS._is_ngit_root(parent):
                return parent
        return cwd
