import pytest

from ngit.db import KVDB


class TestKVDB():
    @pytest.fixture
    def kvdb(self):
        return KVDB()

    def test_insert(self, kvdb):
        assert kvdb.get('123') is None
        kvdb.insert('123', '234')
        assert kvdb.get('123') == '234'

    def test_overwrite(self, kvdb):
        assert kvdb.get('123') is None
        kvdb.insert('123', '234')
        assert kvdb.get('123') == '234'
        kvdb.insert('123', '2345')
        assert kvdb.get('123') == '2345'
