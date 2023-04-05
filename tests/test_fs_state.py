from dataclasses import dataclass

import pytest

from ngit.cli.branch import create_branch
from ngit.cli.checkout import checkout_branch, checkout_ref
from ngit.cli.commit import create_commit
from ngit.cli.status import workdir_status

from conftest import NGitTest, Context
from mocks import MockFS


# TODO move to db_img?
@dataclass(frozen=True)
class FSEntry:
    path: str  # Relative to root
    content: bytes = b''
    is_dir: bool = False


FSImage = set[FSEntry]


class FSStateTest(NGitTest):
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


class TestCommitAndCheckout(FSStateTest):
    def test_file_content_changes(self, mock_fs: MockFS):
        ref0 = self.initial_commit

        mock_fs.write_file('test', b'testdata')
        ref1 = create_commit('main1')

        mock_fs.write_file('subdir/test2', b'other data')
        ref2 = create_commit('main2')

        mock_fs.write_file('test', b'testdata\nmore data')
        ref3 = create_commit('main3')

        mock_fs.write_file('test', b'')
        ref4 = create_commit('main4')

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

    def test_empty_dirs(self, mock_fs: MockFS):
        ref0 = self.initial_commit

        mock_fs.mkdir('testdir')
        ref1 = create_commit('main1')

        mock_fs.mkdir('testdir/subdir')
        ref2 = create_commit('main2')

        mock_fs.mkdir('testdir/second_subdir')
        ref3 = create_commit('main3')

        checkout_ref(ref0)
        self.expect_fs(set())

        checkout_ref(ref1)
        self.expect_fs({
            FSEntry('testdir', is_dir=True),
        })

        checkout_ref(ref2)
        self.expect_fs({
            # Only leaves shoud be returned, testdir is not in image
            FSEntry('testdir/subdir', is_dir=True),
        })

        checkout_ref(ref3)
        self.expect_fs({
            FSEntry('testdir/subdir', is_dir=True),
            FSEntry('testdir/second_subdir', is_dir=True),
        })

    def test_deletion(self, mock_fs: MockFS):
        ref0 = self.initial_commit

        mock_fs.write_file('testfile', b'testdata')
        mock_fs.mkdir('testdir')
        mock_fs.mkdir('testdir2/subdir')
        mock_fs.write_file('testdir2/subfile', b'testdata2')
        ref1 = create_commit('main1')

        mock_fs.safe_remove('testfile')
        mock_fs.safe_remove('testdir')
        mock_fs.safe_remove('testdir2/subdir')
        mock_fs.safe_remove('testdir2/subfile')
        ref2 = create_commit('main2')

        # recreate files and dirs
        mock_fs.write_file('testfile', b'testdata')
        mock_fs.mkdir('testdir')
        mock_fs.mkdir('testdir2/subdir')
        mock_fs.write_file('testdir2/subfile', b'testdata2')
        ref3 = create_commit('main3')

        checkout_ref(ref0)
        self.expect_fs(set())

        checkout_ref(ref1)
        self.expect_fs({
            FSEntry('testfile', b'testdata'),
            FSEntry('testdir', is_dir=True),
            FSEntry('testdir2/subdir', is_dir=True),
            FSEntry('testdir2/subfile', b'testdata2'),
        })

        checkout_ref(ref2)
        self.expect_fs({
            FSEntry('testdir2', is_dir=True),
        })

        checkout_ref(ref3)
        self.expect_fs({
            FSEntry('testfile', b'testdata'),
            FSEntry('testdir', is_dir=True),
            FSEntry('testdir2/subdir', is_dir=True),
            FSEntry('testdir2/subfile', b'testdata2'),
        })

    def test_file_type_changes(self, mock_fs: MockFS):
        ref0 = self.initial_commit

        mock_fs.write_file('test1', b'testdata1')
        mock_fs.write_file('test2', b'testdata2')
        mock_fs.write_file('test3/subfile', b'testdata3')
        mock_fs.mkdir('test4')
        ref1 = create_commit('main1')

        mock_fs.clean()
        self.expect_fs(set())
        mock_fs.mkdir('test1')
        mock_fs.write_file('test2/subfile', b'new testdata2')
        mock_fs.write_file('test3', b'new testdata3')
        mock_fs.write_file('test4', b'new testdata4')
        ref2 = create_commit('main2')

        mock_fs.clean()
        self.expect_fs(set())
        mock_fs.write_file('test1', b'testdata1')
        mock_fs.write_file('test2', b'testdata2')
        mock_fs.write_file('test3/subfile', b'testdata3')
        mock_fs.mkdir('test4')
        ref3 = create_commit('main3')

        checkout_ref(ref0)
        self.expect_fs(set())

        checkout_ref(ref1)
        self.expect_fs({
            FSEntry('test1', b'testdata1'),
            FSEntry('test2', b'testdata2'),
            FSEntry('test3/subfile', b'testdata3'),
            FSEntry('test4', is_dir=True),
        })

        checkout_ref(ref2)
        self.expect_fs({
            FSEntry('test1', is_dir=True),
            FSEntry('test2/subfile', b'new testdata2'),
            FSEntry('test3', b'new testdata3'),
            FSEntry('test4', b'new testdata4'),
        })

        checkout_ref(ref3)
        self.expect_fs({
            FSEntry('test1', b'testdata1'),
            FSEntry('test2', b'testdata2'),
            FSEntry('test3/subfile', b'testdata3'),
            FSEntry('test4', is_dir=True),
        })

    def test_branch_checkout(self, mock_fs: MockFS):
        create_branch('test')

        mock_fs.write_file('test', b'testdata')
        create_commit('main1')

        checkout_branch('test')
        self.expect_fs(set())

        mock_fs.mkdir('testdir')
        mock_fs.write_file('test', b'new testdata')
        create_commit('test1')

        checkout_branch('main')
        self.expect_fs({
            FSEntry('test', b'testdata'),
        })

        checkout_branch('test')
        self.expect_fs({
            FSEntry('test', b'new testdata'),
            FSEntry('testdir', is_dir=True),
        })


class TestStatus(FSStateTest):
    def expect_changelist(self, expected: set[str]):
        assert expected == {
            f'{change.type.short} {change.path}' for change in workdir_status()
        }

    def test_added_files(self, mock_fs: MockFS):
        mock_fs.write_file('test1', b'testdata1')
        mock_fs.write_file('test2', b'testdata2')
        mock_fs.write_file('test3/subfile', b'testdata3')
        mock_fs.mkdir('test3/subdir')
        mock_fs.mkdir('test4')
        self.expect_changelist({
            '+ test1',
            '+ test2',
            '+ test3/subfile',
            '+ test3/subdir',
            '+ test4',
        })

    def test_deleted_files(self, mock_fs: MockFS):
        mock_fs.write_file('test1', b'testdata1')
        mock_fs.write_file('test2', b'testdata2')
        mock_fs.write_file('test3/subfile', b'testdata3')
        mock_fs.mkdir('test3/subdir')
        mock_fs.mkdir('test4')
        create_commit('test')

        mock_fs.clean()
        self.expect_changelist({
            '- test1',
            '- test2',
            '- test3/subfile',
            '- test3/subdir',
            '- test4',
        })

    def test_new_leaf_dir(self, mock_fs: MockFS):
        mock_fs.mkdir('testdir/subdir')
        create_commit('test')

        mock_fs.remove('testdir/subdir')
        self.expect_changelist({
            # Yes, this is not a bug :)
            '- testdir/subdir',
            '+ testdir',
        })

    def test_changed_files(self, mock_fs: MockFS):
        mock_fs.write_file('test1', b'testdata1')
        mock_fs.write_file('test2', b'testdata2')
        mock_fs.write_file('test3', b'testdata3')
        create_commit('test')

        mock_fs.write_file('test1', b'testdata1\nmore data')
        mock_fs.write_file('test2', b'newtestdata2')
        mock_fs.write_file('test3', b'')
        self.expect_changelist({
            'M test1',
            'M test2',
            'M test3',
        })

    def test_file_types(self, mock_fs: MockFS):
        mock_fs.write_file('test1', b'testdata1')
        mock_fs.mkdir('test2')
        create_commit('test')

        mock_fs.clean()
        mock_fs.mkdir('test1')
        mock_fs.write_file('test2', b'newtestdata2')
        self.expect_changelist({
            'M test1',
            'M test2',
        })
