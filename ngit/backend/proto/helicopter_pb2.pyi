from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddNodeRequest(_message.Message):
    __slots__ = ["content", "parent"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    content: bytes
    parent: str
    def __init__(self, parent: _Optional[str] = ..., content: _Optional[bytes] = ...) -> None: ...

class AddNodeResponse(_message.Message):
    __slots__ = ["node"]
    NODE_FIELD_NUMBER: _ClassVar[int]
    node: Node
    def __init__(self, node: _Optional[_Union[Node, _Mapping]] = ...) -> None: ...

class GetNodesRequest(_message.Message):
    __slots__ = ["last", "root"]
    LAST_FIELD_NUMBER: _ClassVar[int]
    ROOT_FIELD_NUMBER: _ClassVar[int]
    last: str
    root: str
    def __init__(self, root: _Optional[str] = ..., last: _Optional[str] = ...) -> None: ...

class GetNodesResponse(_message.Message):
    __slots__ = ["nodes"]
    NODES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[Node]
    def __init__(self, nodes: _Optional[_Iterable[_Union[Node, _Mapping]]] = ...) -> None: ...

class Node(_message.Message):
    __slots__ = ["content", "lseq", "parent"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    LSEQ_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    content: bytes
    lseq: str
    parent: str
    def __init__(self, lseq: _Optional[str] = ..., parent: _Optional[str] = ..., content: _Optional[bytes] = ...) -> None: ...
