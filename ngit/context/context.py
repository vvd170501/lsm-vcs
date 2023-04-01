from os import environ, getcwd

from ..backend import BaseBackend, HelicopterBackend
from ..fs import BaseFS, LocalFS

__all__ = ['get_context']


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Context(metaclass=Singleton):
    def __init__(self, fs: BaseFS, server: BaseBackend) -> None:
        self._fs = fs
        self._server = server

    @property
    def fs(self):
        return self._fs

    @property
    def server(self):
        return self._server


_context = None


# A separate function is used to allow monkeypatching
# (if get_context is imported into another module, it won't be patched)
def _get_context() -> Context:
    global _context
    if _context is None:
        _context = Context(
            LocalFS(getcwd()),
            HelicopterBackend(
                environ.get('HELICOPTER_ADDRESS', 'localhost'),
                int(environ.get('HELICOPTER_PORT', '8888'))
            )
        )
    return _context


def get_context() -> Context:
    return _get_context()
