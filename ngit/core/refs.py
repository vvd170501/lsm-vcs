from base64 import b64decode, b64encode
from collections.abc import Iterator
from dataclasses import dataclass

from ..backend import NodeId
from ..context import get_context
from .nodes import NodeName, resolve_named_node

__all__ = ['get_head', 'set_head']


RefId = NodeId


def ref_to_str(ref: RefId) -> str:
    return b64encode(ref.encode()).decode()


def parse_ref(s: str) -> RefId:
    return b64decode(s).decode()


def get_head() -> tuple[NodeId, str]:
    """Returns (ref, branch)"""
    return get_context().fs.read_file('.ngit/HEAD').decode().split('/')


def set_head(ref: NodeId, branch: str = '') -> None:
    get_context().fs.write_file('.ngit/HEAD', f'{ref}/{branch}'.encode())


@dataclass
class Branch:
    name: str
    ref: RefId

    def __bool__(self):
        return self.ref != '[del]'


def get_branch_events() -> Iterator[Branch]:
    ctx = get_context()
    for node in ctx.server.get_nodes(resolve_named_node(NodeName.BRANCH_EVENTS)):
        name, ref = node.content.decode().split('/')
        yield Branch(name, ref)


def update_branch(branch: Branch) -> None:
    get_context().server.add_node(resolve_named_node(NodeName.BRANCH_EVENTS), f'{branch.name}/{branch.ref}'.encode())
