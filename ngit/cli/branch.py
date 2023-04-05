import click

from ..core.refs import Branch, get_branch_events, get_head, update_branch
from .common import require_repo
from .checkout import try_checkout_branch


@click.command()
@click.argument('branch', required=False)
@click.option('-b', 'chout', is_flag=True, help='Create and checkout branch.')
@require_repo
def branch(branch: str | None, chout: bool):
    if branch is not None:
        create_branch(branch)
        if chout:
            assert try_checkout_branch(branch)
    else:
        if chout:
            click.echo('Error: no branch specified.')
            return
        branches = list_branches()
        _, curr_branch = get_head()
        for branch in branches:
            if not curr_branch:
                click.echo(branch)
            elif branch == curr_branch:
                click.secho('* ' + branch, fg='green')
            else:
                click.echo('  ' + branch)


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
    update_branch(Branch(new_branch_name, get_head()[0]))


def list_branches() -> list[str]:
    """Returns sorted list of branch names."""
    branches = set()
    for branch in get_branch_events():
        if not branch:  # The branch was deleted
            branches.discard(branch.name)
        else:
            branches.add(branch.name)

    return sorted(branches)
