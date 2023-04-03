from abc import ABC, abstractmethod


__all__ = ['BaseDB', 'DBKey']


DBKey = tuple[bytes, str]


class BaseDB(ABC):
    @abstractmethod
    def insert(self, key: DBKey, value: str | bytes) -> None:
        """Writes the key-value pair into the DB"""
        pass

    @abstractmethod
    def get(self, key: DBKey) -> str | bytes | None:
        pass

    @abstractmethod
    def filter(self, key_start: str) -> list[DBKey]:
        """Get all keys key such that key[1] starts with key_start sorted by key[1]"""
        pass

    @abstractmethod
    def filter_by_commit(self, commit: bytes) -> list[DBKey]:
        pass
