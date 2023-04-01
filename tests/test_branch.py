import pickle
import pytest

from ngit.cli.branch import _create_branch, _list_branches

from conftest import NGitTest, Context


class TestBranch(NGitTest):
    FILES = {
        '.ngit/HEAD': b'111'
    }

    @pytest.fixture(autouse=True)
    def setup_server(self, mock_context: Context):
        branches_node_id = mock_context.server.add_node('', b'')
        mock_context.fs.write_file('.ngit/node_ids', pickle.dumps({
            'branch': branches_node_id,
        }))
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
