import click

from ..core.nodes import create_named_node, resolve_named_node
from ..core.refs import set_head_ref


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
    root_id = create_named_node('', 'root', content='ngit_project_root')
    # Branch events: create / update / delete
    create_named_node(root_id, 'branch')
    # Commit tree. Each commit contains a reference to its parent and references to related file changes
    create_named_node(root_id, 'commit')
    # File changes
    create_named_node(root_id, 'fs')
    set_head_ref('')  # Create main branch?


def unpack_project(project_id: str):
    # The project must already exist in the local DB replica.
    if resolve_named_node('root'):
        raise click.ClickException('Project is already initialized, cannot change id')
    if not project_id:
        raise click.ClickException('Project id must not be empty')
    pass  # TODO!!
