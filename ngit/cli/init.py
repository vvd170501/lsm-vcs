from base64 import b64decode

import click

from ..backend import NodeId
from ..context import get_context
from ..core.nodes import assign_name, create_named_node, resolve_named_node
from ..core.refs import set_head


class NodeNames:
    ROOT = 'root'
    # create / update / delete
    BRANCH_EVENTS = 'branch'
    # Each commit contains a reference to its parent (builtin) and references to related file changes
    COMMIT_TREE = 'commit'
    FS = 'fs'  # File changes


@click.command()
@click.argument('project_id', required=False)
def init(project_id: str | None = None):
    """
    Initialize a new or existing project.
    If PROJECT-ID is provided, it must be an id from "ngit project-id" on another replica.'
    """
    if project_id is None:
        init_project()
    else:
        unpack_project(project_id)


def init_project():
    if resolve_named_node('root'):
        # Already initialized
        return
    root_id = create_named_node('', NodeNames.ROOT, content='ngit_project_root')
    create_named_node(root_id, NodeNames.BRANCH_EVENTS)
    commit_tree_root = create_named_node(root_id, NodeNames.COMMIT_TREE)
    create_named_node(root_id, NodeNames.FS)
    set_head(commit_tree_root)  # Create main branch?


def unpack_project(project_id: str):
    # The project must already exist in the local DB replica.
    if resolve_named_node(NodeNames.ROOT):
        raise click.ClickException('Project is already initialized, cannot change id')
    if not project_id:
        raise click.ClickException('Project id must not be empty')
    root_node: NodeId = b64decode(project_id).decode()
    subnodes = get_context().server.get_nodes(root_node)  # TODO limit
    try:
        assign_name(next(subnodes).id, NodeNames.BRANCH_EVENTS)
        commit_tree_root = assign_name(next(subnodes).id, NodeNames.COMMIT_TREE)
        assign_name(next(subnodes).id, NodeNames.FS)
        assign_name(root_node, NodeNames.ROOT)
        set_head(commit_tree_root)  # Use main branch?
    except StopIteration:
        raise click.ClickException(f'Project {project_id} doesn\'t exist')
