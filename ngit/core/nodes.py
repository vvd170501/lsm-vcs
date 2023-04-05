import pickle

from ..backend import NodeId
from ..context import get_context

__all__ = ['resolve_named_node', 'create_named_node']


class NodeName:
    ROOT = 'root'
    # create / update / delete
    BRANCH_EVENTS = 'branch'
    # Each commit contains a reference to its parent (builtin) and references to related file changes
    COMMIT_TREE = 'commit'
    FS = 'fs'  # File changes


def _get_node_ids() -> dict[bytes, NodeId]:
    data = get_context().fs.read_file('.ngit/node_ids')
    return pickle.loads(data) if data else {}


def resolve_named_node(name: str | bytes) -> NodeId:
    if isinstance(name, str):
        name = name.encode()
    # TODO cache node_ids
    return _get_node_ids().get(name, NodeId())


def assign_name(node_id: NodeId, name: str | bytes) -> NodeId:
    if isinstance(name, str):
        name = name.encode()
        ctx = get_context()
    node_ids = _get_node_ids()
    # Add reverse index for faster lookup? In general, there shouldn't be many named nodes
    if node_id in node_ids.values():
        raise RuntimeError(f'Node "{node_id}" already has a name)')
    node_ids[name] = node_id
    ctx.fs.write_file('.ngit/node_ids', pickle.dumps(node_ids))
    return node_id


def create_named_node(parent: NodeId, name: str | bytes, content: str | bytes = b'', exist_ok: bool = False) -> NodeId:
    if isinstance(name, str):
        name = name.encode()
        ctx = get_context()
    node_ids = _get_node_ids()
    if name in node_ids:
        if not exist_ok:
            raise RuntimeError(f'Named nodes must be unique (node "{name!r}" already exists)')
        return node_ids[name]
    if isinstance(content, str):
        content = content.encode()
    node_ids[name] = ctx.server.add_node(parent, content)
    ctx.fs.write_file('.ngit/node_ids', pickle.dumps(node_ids))
    return node_ids[name]
