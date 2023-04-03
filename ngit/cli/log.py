from base64 import b64encode
from collections.abc import Iterator

import click

from ..backend import Node
from ..context import get_context
from ..core.nodes import NodeName, resolve_named_node
from ..core.refs import get_head
from .common import require_repo


@click.command()
@require_repo
def log(**kwargs):
    for commit in _log(**kwargs):
        # TODO use hash-based commit ids?
        print(f'{b64encode(commit.id.encode()).decode()} {commit.content.decode()}')


def _log() -> Iterator[Node]:
    commit_tree = resolve_named_node(NodeName.COMMIT_TREE)
    # TODO use direct access to DB for more efficien GETs?
    # Currently we get the whole tree, because there's no suitable API
    head, _ = get_head()
    nodes = {node.id: node for node in get_context().server.get_nodes(commit_tree)}
    while head != commit_tree:
        yield nodes[head]
        head = nodes[head].parent
