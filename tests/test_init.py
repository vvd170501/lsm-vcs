from typing import Callable

import pytest

from ngit.cli.init import init_project, unpack_project
from ngit.cli.project_id import get_project_id

from conftest import NGitTest, Context
from mocks import MockBackend, MockFS


class TestInit(NGitTest):
    AUTO_INIT = False

    def test_multiple_projects(self, mock_context: Context, use_context: Callable[[Context], Context]) -> None:
        init_project()
        id1 = get_project_id()
        with use_context(Context(MockFS(), mock_context.server)):
            init_project()
            id2 = get_project_id()
        with use_context(Context(MockFS(), mock_context.server)):
            init_project()
            id3 = get_project_id()
        # Check that ids are unique
        assert len({id1, id2, id3}) == 3

    def test_unpack_project(self, mock_context: Context, use_context: Callable[[Context], Context]) -> None:
        init_project()
        proj_id = get_project_id()
        with use_context(Context(MockFS(), mock_context.server)):
            init_project()
            other_proj_id = get_project_id()
            assert other_proj_id != proj_id

        with use_context(Context(MockFS(), mock_context.server)):
            unpack_project(proj_id)
            assert get_project_id() == proj_id
        with use_context(Context(MockFS(), mock_context.server)):
            unpack_project(other_proj_id)
            assert get_project_id() == other_proj_id

    def test_init_in_repo(self):
        init_project()
        proj_id = get_project_id()
        init_project()
        assert get_project_id() == proj_id

    def test_unpack_in_repo(self, mock_context: Context, use_context: Callable[[Context], Context]) -> None:
        init_project()
        proj_id = get_project_id()
        with use_context(Context(MockFS(), mock_context.server)):
            init_project()
            other_proj_id = get_project_id()
            assert other_proj_id != proj_id

            with pytest.raises(Exception, match='Project is already initialized, cannot unpack'):
                unpack_project(other_proj_id)
            with pytest.raises(Exception, match='Project is already initialized, cannot re-init'):
                unpack_project(proj_id)

    def test_unpack_unknown_id(self, mock_context: Context, use_context: Callable[[Context], Context]) -> None:
        with use_context(Context(MockFS(), MockBackend())):
            init_project()
            proj_id = get_project_id()
        with use_context(Context(MockFS(), MockBackend())):
            with pytest.raises(Exception, match=f'Project {proj_id} doesn\'t exist'):
                unpack_project(proj_id)
