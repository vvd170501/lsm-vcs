import pytest

import ngit.context
from ngit.context.context import Context
from ngit.cli.init import _init

from mocks import MockFS, MockBackend


class NGitTest:
    @pytest.fixture(autouse=True)
    def mock_context(self, monkeypatch) -> Context:
        context = Context(MockFS(), MockBackend())

        def get_mock_context():
            return context

        monkeypatch.setattr(ngit.context.context, '_get_context', get_mock_context)
        return context

    @pytest.fixture(autouse=True)
    def init_repo(self, mock_context: Context) -> None:
        _init()
