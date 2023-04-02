import click

from ..context import get_context
from ..core.nodes import resolve_named_node
from ..core.refs import get_branch_events, get_head


@click.command()
@click.argument('branch', required=False)
def branch(branch: str | None):
    if branch is not None:
        create_branch(branch)
    else:
        branches = list_branches()
        click.echo('\n'.join(branches))  # mark current branch?


def create_branch(new_branch_name: str):
    if not new_branch_name:
        raise click.ClickException('Empty branch name is not allowed')
    exists = False
    # TODO optimize.
    # - Use reverse order. If the last event wasn't a deletion, then the branch exists
    # - Store last_id for each branch in .ngit to reduce number of traversed nodes
    # - Use a separate subtree for ech branch
    for branch in get_branch_events():
        if branch.name == new_branch_name:
            exists = bool(branch)
    if exists:
        raise click.exceptions.ClickException(f'Branch "{new_branch_name}" already exists')
    get_context().server.add_node(resolve_named_node('branch'), f'{new_branch_name}/{get_head()[0]}'.encode())


def list_branches() -> list[str]:
    """Returns sorted list of branch names."""
    branches = set()
    for branch in get_branch_events():
        if not branch:  # The branch was deleted
            branches.discard(branch.name)
        else:
            branches.add(branch.name)

    return sorted(branches)
