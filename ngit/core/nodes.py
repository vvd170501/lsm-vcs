import pickle

from ..backend import NodeId
from ..context import get_context

__all__ = ['resolve_named_node', 'create_named_node']


def _get_node_ids() -> dict[bytes, NodeId]:
    data = get_context().fs.read_file('.ngit/node_ids')
    return pickle.loads(data) if data else {}


def resolve_named_node(name: str | bytes) -> NodeId:
    if isinstance(name, str):
        name = name.encode()
    # TODO cache node_ids
    return _get_node_ids().get(name, NodeId())


def create_named_node(parent: NodeId, name: str | bytes, exist_ok: bool = False) -> NodeId:
    if isinstance(name, str):
        name = name.encode()
        ctx = get_context()
    node_ids = _get_node_ids()
    if name in node_ids:
        if not exist_ok:
            raise RuntimeError(f'Named nodes must be unique (node "{name}" already exists)')
        return node_ids[name]
    node_ids[name] = ctx.server.add_node(parent, b'')
    ctx.fs.write_file('.ngit/node_ids', pickle.dumps(node_ids))
    return node_ids[name]
