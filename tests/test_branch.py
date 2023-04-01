from ngit.cli.branch import _create_branch, _list_branches

from conftest import NGitTest


class TestBranch(NGitTest):
    NODES = []  # TODO

    def test_list_branches(self):
        # Not sure, maybe it's better to check stdout. After all, we're testing a CLI app
        assert _list_branches() == ['main', 'test']

    def test_create_branch(self):
        _create_branch('test2')
        assert _list_branches() == ['main', 'test', 'test2']
