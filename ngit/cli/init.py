from base64 import b64decode

import click

from ..backend import NodeId
from ..context import get_context
from ..core.nodes import NodeName, assign_name, create_named_node, resolve_named_node
from ..core.refs import set_head


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
    root_id = create_named_node('', NodeName.ROOT, content='ngit_project_root')
    create_named_node(root_id, NodeName.BRANCH_EVENTS)
    commit_tree_root = create_named_node(root_id, NodeName.COMMIT_TREE)
    create_named_node(root_id, NodeName.FS)
    set_head(commit_tree_root)  # Create main branch?


def unpack_project(project_id: str):
    # The project must already exist in the local DB replica.
    if resolve_named_node(NodeName.ROOT):
        raise click.ClickException('Project is already initialized, cannot re-init')
    if not project_id:
        raise click.ClickException('Project id must not be empty')
    root_node: NodeId = b64decode(project_id).decode()
    subnodes = get_context().server.get_nodes(root_node)  # TODO limit
    try:
        assign_name(next(subnodes).id, NodeName.BRANCH_EVENTS)
        commit_tree_root = assign_name(next(subnodes).id, NodeName.COMMIT_TREE)
        assign_name(next(subnodes).id, NodeName.FS)
        assign_name(root_node, NodeName.ROOT)
        set_head(commit_tree_root)  # Use main branch?
    except StopIteration:
        raise click.ClickException(f'Project {project_id} doesn\'t exist')
