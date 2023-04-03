from sortedcontainers import SortedDict
from bisect import bisect_left, bisect_right
from .db import BaseDB


__all__ = ['KVDB']


class KVDB(BaseDB):
    def __init__(self) -> None:
        self._kv = SortedDict()

    def insert(self, key: str, value: str | bytes) -> None:
        self._kv[key] = value

    def get(self, key: str) -> str | bytes | None:
        if key in self._kv:
            return self._kv[key]
        return None

    def filter(self, key_start: str) -> list[str]:
        def get_str_start(s: str) -> str:
            return s[:min(len(s), len(key_start))]

        keys = self._kv.keys()
        beg = bisect_left(keys, key_start, key=get_str_start)
        end = bisect_right(keys, key_start, key=get_str_start)
        return keys[beg:end]
