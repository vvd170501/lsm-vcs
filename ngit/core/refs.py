from base64 import b64decode, b64encode
from collections.abc import Iterator
from dataclasses import dataclass

from ..backend import Node, NodeId
from ..context import get_context
from .nodes import NodeName, resolve_named_node

__all__ = [
    'ref_to_str', 'parse_ref',
    'get_head', 'set_head',
    'Branch', 'get_branch_events', 'update_branch',
    'iterate_history'
]


RefId = NodeId


def ref_to_str(ref: RefId) -> str:
    return b64encode(ref.encode()).decode()


def parse_ref(s: str) -> RefId:
    return b64decode(s).decode()


def get_head() -> tuple[NodeId, str]:
    """Returns (ref, branch)"""
    return get_context().fs.read_file('.ngit/HEAD').decode().split('/')


def set_head(ref: NodeId, branch: str) -> None:
    # empty branch name = detached HEAD
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


def iterate_history(commit: RefId) -> Iterator[Node]:
    commit_tree = resolve_named_node(NodeName.COMMIT_TREE)
    # TODO use direct access to DB for more efficien GETs?
    # Currently we get the whole tree, because there's no suitable API
    nodes = {node.id: node for node in get_context().server.get_nodes(commit_tree)}
    while commit != commit_tree:
        yield nodes[commit]
        commit = nodes[commit].parent


def get_branch_id(branch_name: str) -> RefId | None:
    target_branch = None
    for branch in get_branch_events():
        if branch.name == branch_name:
            target_branch = branch.ref
            # no break, need to get the latest event. TODO use reverse order?
    return target_branch
