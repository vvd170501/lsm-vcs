from collections.abc import Iterator
from dataclasses import dataclass

from ..backend import NodeId
from ..context import get_context
from .nodes import resolve_named_node

__all__ = ['get_head', 'set_head_ref']


def get_head() -> tuple[NodeId, str]:
    """Returns (ref, branch)"""
    return get_context().fs.read_file('.ngit/HEAD').decode().split('/')


def set_head_ref(ref: NodeId, branch: str = '') -> None:
    get_context().fs.write_file('.ngit/HEAD', f'{branch}/{ref}'.encode())


@dataclass
class Branch:
    name: str
    ref: NodeId

    def __bool__(self):
        return self.ref != '[del]'


def get_branch_events() -> Iterator[Branch]:
    ctx = get_context()
    for node in ctx.server.get_nodes(resolve_named_node('branch')):
        name, ref = node.content.decode().split('/')
        yield Branch(name, ref)