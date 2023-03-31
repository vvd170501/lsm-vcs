from os import environ, getcwd

from ..backend import BaseServer, HelicopterServer
from ..fs import BaseFS, LocalFS

__all__ = ['GetContext']


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Context(metaclass=Singleton):
    def __init__(self, fs: BaseFS, server: BaseServer) -> None:
        self._fs = fs
        self._server = server

    @property
    def fs(self):
        return self._fs

    @property
    def server(self):
        return self._server


_context = None


def GetContext() -> Context:  # Add args for first call?
    global _context
    if _context is None:
        _context = Context(
            LocalFS(getcwd()),
            HelicopterServer(
                environ.get('HELICOPTER_ADDRESS', 'localhost'),
                int(environ.get('HELICOPTER_PORT', '8888'))
            )
        )
    return _context
