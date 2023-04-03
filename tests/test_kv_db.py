import pytest

from ngit.db import KVDB


class TestKVDB():
    @pytest.fixture
    def kvdb(self):
        return KVDB()

    def test_insert(self, kvdb):
        assert kvdb.get((b'', '123')) is None
        kvdb.insert((b'', '123'), '234')
        assert kvdb.get((b'', '123')) == '234'

    def test_overwrite(self, kvdb):
        assert kvdb.get((b'', '123')) is None
        kvdb.insert((b'', '123'), '234')
        assert kvdb.get((b'', '123')) == '234'
        kvdb.insert((b'', '123'), '2345')
        assert kvdb.get((b'', '123')) == '2345'

    def test_filter(self, kvdb):
        kvdb.insert((b'', '100'), '1')
        kvdb.insert((b'', '101'), '1')
        kvdb.insert((b'', '000'), '1')
        kvdb.insert((b'', '110'), '1')
        kvdb.insert((b'', '1000'), '1')
        assert kvdb.filter('10') == [(b'', '100'), (b'', '1000'), (b'', '101')]

    def test_empty_filter(self, kvdb):
        assert kvdb.filter('1') == []
        kvdb.insert((b'', '0'), 1)
        assert kvdb.filter('1') == []

    def test_filter_by_commit(self, kvdb):
        kvdb.insert((b'0', '100'), '1')
        kvdb.insert((b'1', '101'), '1')
        kvdb.insert((b'0', '000'), '1')
        kvdb.insert((b'1', '110'), '1')
        kvdb.insert((b'2', '1000'), '1')
        assert kvdb.filter_by_commit(b'0') == [(b'0', '000'), (b'0', '100')]
        assert kvdb.filter_by_commit(b'1') == [(b'1', '101'), (b'1', '110')]
        assert kvdb.filter_by_commit(b'2') == [(b'2', '1000')]
        assert kvdb.filter_by_commit(b'3') == []
