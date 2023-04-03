from abc import ABC, abstractmethod


__all__ = ['BaseDB']


class BaseDB(ABC):
    @abstractmethod
    def insert(self, key: tuple[bytes, str], value: str | bytes) -> None:
        """Writes the key-value pair into the DB"""
        pass

    @abstractmethod
    def get(self, key: tuple[bytes, str]) -> str | bytes | None:
        pass

    @abstractmethod
    def filter(self, key_start: str) -> list[tuple[bytes, str]]:
        """Get all keys key such that key[1] starts with key_start sorted by key[1]"""
        pass
