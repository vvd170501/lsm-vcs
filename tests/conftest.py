from contextlib import contextmanager
from os import environ

import pytest

import ngit.context
from ngit.backend import HelicopterBackend
from ngit.context.context import Context
from ngit.cli.init import init_project

from mocks import MockFS, MockBackend


class NGitTest:
    AUTO_INIT = True

    @pytest.fixture(autouse=True)
    def mock_context(self, monkeypatch) -> Context:
        if int(environ.get('USE_HELICOPTER', '0')) > 0:
            backend = HelicopterBackend(
                environ.get('HELICOPTER_ADDRESS', '127.0.0.1'),
                int(environ.get('HELICOPTER_PORT', '8888'))
            )
        else:
            backend = MockBackend()
        context = Context(MockFS(), backend)

        def get_mock_context():
            return context

        monkeypatch.setattr(ngit.context.context, '_get_context', get_mock_context)
        return context

    @pytest.fixture
    def use_context(self, monkeypatch):

        @contextmanager
        def temp_context(context: Context) -> Context:
            def get_context():
                return context
            try:
                with monkeypatch.context() as m:
                    m.setattr(ngit.context.context, '_get_context', get_context)
                    yield context
            finally:
                pass

        return temp_context

    @pytest.fixture(autouse=True)
    def init_repo(self, mock_context: Context) -> None:
        if self.AUTO_INIT:
            init_project()
