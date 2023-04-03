import pytest

from ngit.cli.branch import create_branch
from ngit.cli.checkout import do_checkout
from ngit.cli.commit import create_commit
from ngit.core.refs import RefId, iterate_history

from conftest import NGitTest, Context


class TestCommitHistory(NGitTest):
    @pytest.fixture(autouse=True)
    def setup(self, init_repo, mock_context: Context) -> None:  # init_repo is requested for correct init order
        create_branch('main')
        do_checkout('main')

    def expect_history(self, expected_history: list[tuple[RefId, str]], commit: RefId | None = None):
        if commit is None:
            commit = self.head
        assert [
            (commit.id, commit.content.decode()) for commit in iterate_history(commit)
        ] == expected_history

    def test_commit_and_log(self):
        assert self.active_branch == 'main'
        ref0 = self.head

        ref1 = create_commit('main1')
        assert self.active_branch == 'main'
        ref2 = create_commit('main2')
        assert self.active_branch == 'main'

        assert len({ref0, ref1, ref2}) == 3
        self.expect_history([
            (ref2, 'main2'),
            (ref1, 'main1'),
        ])

    def test_commit_and_checkout_branches(self):
        create_branch('test')
        assert self.active_branch == 'main'
        main1 = create_commit('main1')
        main2 = create_commit('main2')
        assert self.active_branch == 'main'

        do_checkout('test')
        assert self.active_branch == 'test'
        self.expect_history([])
        test1 = create_commit('test1')
        test2 = create_commit('test2')
        assert self.active_branch == 'test'

        assert test2 != main2

        # Check that we can switch back
        do_checkout('main')
        self.expect_history([
            (main2, 'main2'),
            (main1, 'main1'),
        ])
        # Switch to test again, just in case
        do_checkout('test')
        self.expect_history([
            (test2, 'test2'),
            (test1, 'test1'),
        ])

    @pytest.mark.skip(reason='Need to separate ref parsing and checkout')
    def test_commit_and_checkout_detached(self):
        assert self.active_branch == 'main'
        main1 = create_commit('main1')
        main2 = create_commit('main2')
        assert self.active_branch == 'main'

        # Detach and create some commits
        do_checkout(main1)
        assert not self.active_branch
        self.expect_history([main1, 'main1'])
        fork1 = create_commit('fork1')
        fork2 = create_commit('fork2')
        assert fork2 != main2
        self.expect_history([
            (fork2, 'fork2'),
            (fork1, 'fork1'),
            (main1, 'main1')
        ])

        # check that main wasn't moved and that we still can commit to it
        do_checkout('main')
        assert self.head == main2
        main3 = create_commit('main3')
        self.expect_history([
            (main3, 'main3'),
            (main2, 'main2'),
            (main1, 'main1'),
        ])
