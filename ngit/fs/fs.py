from abc import ABC, abstractmethod
from collections.abc import Iterator
from os import PathLike

__all__ = ['BaseFS']


class BaseFS(ABC):
    @abstractmethod
    def read_file(self, path: str | PathLike) -> bytes | None:
        """Returns contents of the file or None if the file doesn't exist. Symlinks are not supported."""
        pass

    @abstractmethod
    def write_file(self, path: str | PathLike, content: bytes) -> int:
        pass

    @abstractmethod
    def mkdir(self, path: str | PathLike) -> None:
        pass

    @abstractmethod
    def remove(self, path: str | PathLike) -> None:  # Unused?
        """Removes a file or a directory, recursively. If the file doesn't exist, does nothing."""
        pass

    @abstractmethod
    def clean(self) -> None:
        """Removes all files and dirs except '/.ngit'."""
        pass

    @abstractmethod
    def is_dir(self, path: str | PathLike) -> bool:
        pass

    @abstractmethod
    def rec_iter(self) -> Iterator[str]:
        """Yields root-relative paths to all files and empty directories, excluding ones named '.ngit'."""
        pass

    @property
    @abstractmethod
    def is_ngit_repo(self) -> bool:
        pass

    @property
    @abstractmethod
    def root(self) -> str | PathLike:
        pass
