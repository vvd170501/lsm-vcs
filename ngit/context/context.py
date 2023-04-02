from os import environ

from ..backend import BaseBackend, HelicopterBackend
from ..fs import BaseFS, LocalFS

__all__ = ['get_context']


class Context:
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
            LocalFS(),
            HelicopterBackend(
                environ.get('HELICOPTER_ADDRESS', '127.0.0.1'),
                int(environ.get('HELICOPTER_PORT', '8888'))
            )
        )
    return _context


def get_context() -> Context:
    return _get_context()
