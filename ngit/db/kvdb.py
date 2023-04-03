from sortedcontainers import SortedDict, SortedSet
from bisect import bisect_left, bisect_right
from .db import BaseDB, DBKey


__all__ = ['KVDB']


class KVDB(BaseDB):
    def __init__(self) -> None:
        self._kv = SortedDict()
        self._transposed_keys = SortedSet()

    def insert(self, key: DBKey, value: str | bytes) -> None:
        self._kv[key] = value
        self._transposed_keys.add((key[1], key[0]))

    def get(self, key: DBKey) -> str | bytes | None:
        if key in self._kv:
            return self._kv[key]
        return None

    def filter(self, key_start: str) -> list[DBKey]:
        def get_str_start(s: tuple[str, bytes]) -> str:
            return s[0][:min(len(s[0]), len(key_start))]

        keys = list(self._transposed_keys)
        beg = bisect_left(keys, key_start, key=get_str_start)
        end = bisect_right(keys, key_start, key=get_str_start)
        return list(map(lambda x: (x[1], x[0]), keys[beg:end]))

    def filter_by_commit(self, commit: bytes) -> list[DBKey]:
        commits = list(map(lambda x: x[0], self._kv.keys()))
        beg = bisect_left(commits, commit)
        end = bisect_right(commits, commit)
        return self._kv.keys()[beg:end]
