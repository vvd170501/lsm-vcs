from dataclasses import dataclass

import pytest

from ngit.cli.branch import create_branch
from ngit.cli.checkout import checkout_branch, checkout_ref
from ngit.cli.commit import create_commit

from conftest import NGitTest, Context


@dataclass(frozen=True)
class FSEntry:
    path: str  # Relative to root
    content: bytes = b''
    is_dir: bool = False


FSImage = set[FSEntry]


class TestFSState(NGitTest):
    @pytest.fixture(autouse=True)
    def setup(self, init_repo, mock_context: Context) -> None:  # init_repo is requested for correct init order
        self._mock_context = mock_context
        create_branch('main')
        checkout_branch('main')
        self.initial_commit = create_commit('Initial commit')

    def write_fs(self, image: FSImage, context: Context | None = None):
        if context is None:
            context = self._mock_context  # Can we use the fixture directly?
        fs = context.fs
        fs.clean()
        for entry in image:
            if entry.is_dir:
                fs.mkdir(entry.path)
            else:
                fs.write_file(entry.path, entry.content)

    def expect_fs(self, expected_image: FSImage, context: Context | None = None):
        if context is None:
            context = self._mock_context  # Can we use the fixture directly?
        fs = context.fs
        image: FSImage = set()
        for file in fs.rec_iter():
            if fs.is_dir(file):
                image.add(FSEntry(file, is_dir=True))
            else:
                image.add(FSEntry(file, fs.read_file(file)))
        assert image == expected_image

    def test_create_file(self, mock_context: Context):
        ref0 = self.initial_commit
        mock_context.fs.write_file('test', b'testdata')
        ref1 = create_commit('main1')
        mock_context.fs.write_file('subdir/test2', b'other data')
        ref2 = create_commit('main2')
        mock_context.fs.write_file('test', b'testdata\nmore data')
        ref3 = create_commit('main2')
        mock_context.fs.write_file('test', b'')
        ref4 = create_commit('main2')
        checkout_ref(ref0)
        self.expect_fs(set())
        checkout_ref(ref1)
        self.expect_fs({
            FSEntry('test', b'testdata'),
        })
        checkout_ref(ref2)
        self.expect_fs({
            FSEntry('test', b'testdata'),
            FSEntry('subdir/test2', b'other data')
        })
        checkout_ref(ref3)
        self.expect_fs({
            FSEntry('test', b'testdata\nmore data'),
            FSEntry('subdir/test2', b'other data')
        })
        checkout_ref(ref4)
        self.expect_fs({
            FSEntry('test', b''),
            FSEntry('subdir/test2', b'other data')
        })

    # TODO empty dirs, deletion, checkout branch
