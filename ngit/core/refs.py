from collections.abc import Iterator
from typing import NamedTuple

from ..backend import NodeId
from ..context import get_context
from .nodes import resolve_named_node

__all__ = ['get_head_ref', 'set_head_ref']


def get_head_ref() -> NodeId:
    return get_context().fs.read_file('.ngit/HEAD').decode()


def set_head_ref(ref: NodeId) -> None:
    get_context().fs.write_file('.ngit/HEAD', ref.encode())


Branch = NamedTuple('Branch', [('name', str), ('ref', NodeId)])


def get_branch_events() -> Iterator[Branch]:
    ctx = get_context()
    for node in ctx.server.get_nodes(resolve_named_node('branch')):
        name, ref = node.content.decode().split('/')
        yield Branch(name, ref)
