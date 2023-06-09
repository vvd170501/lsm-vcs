import pytest

from ngit.cli.branch import create_branch, list_branches
from ngit.core.nodes import resolve_named_node

from conftest import NGitTest, Context


class TestBranch(NGitTest):
    @pytest.fixture(autouse=True)
    def setup(self, init_repo, mock_context: Context) -> None:  # init_repo is requested for correct init order
        branches_node_id = resolve_named_node('branch')
        assert branches_node_id
        # TODO use "commit" instead?
        # Pros: the test doesn't depend on storage implementation
        # Cons: tests become dependent on each other, it'll be harder to debug them
        mock_context.server.add_node(branches_node_id, b'main/123')
        mock_context.server.add_node(branches_node_id, b'test/456')
        mock_context.server.add_node(branches_node_id, b'main/789')  # Ref was updated
        mock_context.server.add_node(branches_node_id, b'test/')  # The branch was deleted
        mock_context.server.add_node(branches_node_id, b'test/987')  # Re-created

    def test_list_branches(self):
        # Not sure, maybe it's better to check stdout. After all, we're testing a CLI app
        assert list_branches() == ['main', 'test']

    def test_create_branch(self):
        create_branch('test2')
        assert list_branches() == ['main', 'test', 'test2']

    def test_create_branch_already_exists(self):
        assert list_branches() == ['main', 'test']
        create_branch('test2')
        with pytest.raises(Exception, match='Branch "test2" already exists'):
            create_branch('test2')

    def test_create_branch_bad_names(self):
        with pytest.raises(Exception, match='Empty branch name is not allowed'):
            create_branch('')
        with pytest.raises(Exception, match='Cannot create branch: "HEAD" is reserved'):
            create_branch('HEAD')
