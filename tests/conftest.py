import pytest

import ngit.context
from ngit.context.context import Context

from mocks import MockFS, MockBackend


class NGitTest:
    # FILES = {
    #     '.ngit/HEAD': b'123456',  # ref
    #     'some_dir/file.txt': 'Some text\n',
    # }
    FILES: dict[str, bytes] = {}  # Not sure, maybe it will be easier to call write_file manually

    @pytest.fixture(autouse=True)
    def mock_context(self, monkeypatch) -> Context:
        context = Context(MockFS(self.FILES), MockBackend())
        # TODO add some initial nodes?

        def get_mock_context():
            return context

        monkeypatch.setattr(ngit.context.context, '_get_context', get_mock_context)
        return context
