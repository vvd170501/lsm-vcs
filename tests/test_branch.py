import pytest

from ngit.cli.branch import _create_branch, _list_branches
from ngit.core.nodes import resolve_named_node

from conftest import NGitTest, Context


class TestBranch(NGitTest):

    @pytest.fixture(autouse=True)
    def setup(self, init_repo, mock_context: Context) -> None:
        branches_node_id = resolve_named_node('branch')
        assert branches_node_id
        mock_context.server.add_node(branches_node_id, b'main/123')
        mock_context.server.add_node(branches_node_id, b'test/456')
        mock_context.server.add_node(branches_node_id, b'main/789')  # Ref was updated
        mock_context.server.add_node(branches_node_id, b'test/')  # The branch was deleted
        mock_context.server.add_node(branches_node_id, b'test/987')  # Re-created

    def test_list_branches(self):
        # Not sure, maybe it's better to check stdout. After all, we're testing a CLI app
        assert _list_branches() == ['main', 'test']

    def test_create_branch(self):
        _create_branch('test2')
        assert _list_branches() == ['main', 'test', 'test2']
