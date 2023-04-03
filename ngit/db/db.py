from abc import ABC, abstractmethod


__all__ = ['BaseDB']


class BaseDB(ABC):
    @abstractmethod
    def insert(self, key: str, value: str) -> None:
        """Writes the key-value pair into the DB"""
        pass

    @abstractmethod
    def get(self, key: str) -> str:
        pass

    @abstractmethod
    def filter(self, key_start: str) -> list[str]:
        """Get all keys starting with key_start in lexicographic order"""
        pass
