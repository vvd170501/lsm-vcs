from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DBItems(_message.Message):
    __slots__ = ["items", "replica_id"]
    class DbItem(_message.Message):
        __slots__ = ["key", "lseq", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        LSEQ_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        lseq: str
        value: str
        def __init__(self, lseq: _Optional[str] = ..., key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    REPLICA_ID_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[DBItems.DbItem]
    replica_id: int
    def __init__(self, items: _Optional[_Iterable[_Union[DBItems.DbItem, _Mapping]]] = ..., replica_id: _Optional[int] = ...) -> None: ...

class EventsRequest(_message.Message):
    __slots__ = ["key", "limit", "lseq", "replica_id"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    LSEQ_FIELD_NUMBER: _ClassVar[int]
    REPLICA_ID_FIELD_NUMBER: _ClassVar[int]
    key: str
    limit: int
    lseq: str
    replica_id: int
    def __init__(self, replica_id: _Optional[int] = ..., lseq: _Optional[str] = ..., key: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class LSeq(_message.Message):
    __slots__ = ["lseq"]
    LSEQ_FIELD_NUMBER: _ClassVar[int]
    lseq: str
    def __init__(self, lseq: _Optional[str] = ...) -> None: ...

class PutRequest(_message.Message):
    __slots__ = ["key", "value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class ReplicaKey(_message.Message):
    __slots__ = ["key", "replica_id"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    REPLICA_ID_FIELD_NUMBER: _ClassVar[int]
    key: str
    replica_id: int
    def __init__(self, key: _Optional[str] = ..., replica_id: _Optional[int] = ...) -> None: ...

class SeekGetRequest(_message.Message):
    __slots__ = ["key", "limit", "lseq"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    LSEQ_FIELD_NUMBER: _ClassVar[int]
    key: str
    limit: int
    lseq: str
    def __init__(self, lseq: _Optional[str] = ..., key: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class SyncGetRequest(_message.Message):
    __slots__ = ["replica_id"]
    REPLICA_ID_FIELD_NUMBER: _ClassVar[int]
    replica_id: int
    def __init__(self, replica_id: _Optional[int] = ...) -> None: ...

class Value(_message.Message):
    __slots__ = ["lseq", "value"]
    LSEQ_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    lseq: str
    value: str
    def __init__(self, value: _Optional[str] = ..., lseq: _Optional[str] = ...) -> None: ...
