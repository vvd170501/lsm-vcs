from abc import ABC, abstractmethod
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
