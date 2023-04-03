from abc import ABC, abstractmethod
from collections.abc import Iterable
from os import PathLike

__all__ = ['BaseFS']


class BaseFS(ABC):
    @abstractmethod
    def read_file(self, path: str | PathLike) -> bytes | None:
        """Returns contents of the file or None if the file doesn't exist."""
        pass

    @abstractmethod
    def write_file(self, path: str | PathLike, content: bytes) -> int:
        pass

    @abstractmethod
    def iter_dir(self, path: str | PathLike) -> Iterable:
        pass

    @abstractmethod
    def is_dir(self, path: str | PathLike) -> bool:
        pass

    @property
    @abstractmethod
    def is_ngit_repo(self) -> bool:
        pass

    @property
    @abstractmethod
    def root(self) -> str | PathLike:
        pass
