from sortedcontainers import SortedDict, SortedSet
from bisect import bisect_left, bisect_right
from .db import BaseDB


__all__ = ['KVDB']


class KVDB(BaseDB):
    def __init__(self) -> None:
        self._kv = SortedDict()
        self._transposed_keys = SortedSet()

    def insert(self, key: tuple[bytes, str], value: str | bytes) -> None:
        self._kv[key] = value
        self._transposed_keys.add((key[1], key[0]))

    def get(self, key: tuple[bytes, str]) -> str | bytes | None:
        if key in self._kv:
            return self._kv[key]
        return None

    def filter(self, key_start: str) -> list[tuple[bytes, str]]:
        def get_str_start(s: tuple[str, bytes]) -> str:
            return s[0][:min(len(s[0]), len(key_start))]

        keys = list(self._transposed_keys)
        beg = bisect_left(keys, key_start, key=get_str_start)
        end = bisect_right(keys, key_start, key=get_str_start)
        return list(map(lambda x: (x[1], x[0]), keys[beg:end]))
